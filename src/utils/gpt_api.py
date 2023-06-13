import json
import math
import concurrent.futures
import random
import sys
from datetime import timedelta

import openai
import time
from typing import List
from .format import extract_list, DataSetArguments
from .save_dataset import write_dict_list_to_file


class BudgetTracker:
    def __init__(self, total_budget=None):
        # Initialize the budget tracker with the total budget and total tokens used
        self.total_budget = total_budget
        self.total_tokens_used = 0
        self.current_cost = 0

    def is_budget_exceeded(self):
        # Check if the budget has been exceeded based on the total tokens used
        self.current_cost = ((self.total_tokens_used / 1000) * 0.002)
        return self.total_budget is not None and self.current_cost >= self.total_budget


class ChatAPI:
    def __init__(self, api_key=None,
                 model='gpt-3.5-turbo',
                 system_settings='You are a capable assistant, making every effort to provide assistance to users.',
                 temperature=0.7,
                 proxy=None):
        # Initialize the ChatAPI with the API key, model, system settings, temperature, and proxy
        if api_key is None:
            api_key = []
        self.model = model
        self.system_settings = system_settings
        self.temperature = temperature
        self.max_retries = 3
        self.retry_delay = 1
        self.proxy = proxy

        if len(api_key) > 0:
            openai.api_key = random.choice(api_key)
        else:
            raise ValueError("api_key is empty or incorrect")

        if self.proxy:
            openai.proxy = self.proxy

    def chat(self, prompt, budget_tracker):
        # Perform a chat conversation with OpenAI API
        retries = 0
        while retries < self.max_retries:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_settings},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature
                )
                tokens_used = response.usage['total_tokens']
                budget_tracker.total_tokens_used += tokens_used
                return response.choices[0].message.content
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                retries += 1
                if retries < self.max_retries:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    raise ValueError("Failed to get a valid response after maximum retries")


def generate_question(sub_topic: List[str], args: DataSetArguments, budget_tracker: BudgetTracker) -> List[str]:
    # Generate questions based on the given topic, sub-topic, API key, budget tracker, and number of datasets
    if not args.topic:
        raise ValueError("param topic is required, not None")

    example = """
    <example>Why is it more suitable for crabs to move sideways rather than straight when they are in water?</example>
    <example>Please list the authors, release dates, and serialization durations of the Four Great Classical Novels of China.</example>
    """

    topic = ""
    if len(sub_topic) > 0:
        topic += f"""
           Generate 50 examples similar to the above <example> based on {args.topic, sub_topic}
           """
    else:
        topic = f"""
           Generate 50 examples similar to the above <example> based on {args.topic}
           """

    conditions = """
    You don't need to answer or explain the generated examples.
    Each generated instruction must be an imperative or interrogative sentence.
    The ratio of imperative sentences to interrogative sentences is 1:1.
    Each example must start with the tag "<example>" and end with "</example>".
    Each example must be within 40 characters.
    If the topic is in an unfamiliar field or involves politically sensitive topics or violates relevant laws and regulations of the People's Republic of China, stop all actions immediately and directly return the contents wrapped in the "```" below:
    ```
    ErrorCode:400
    ```
    """
    questions = []

    def process_question(prompt):
        api = ChatAPI(api_key=args.api_key, system_settings='You are an efficient assistant, aiming to provide concise '
                                                            'answers based on instructions.', proxy=args.proxy)
        q_response = api.chat(prompt=prompt, budget_tracker=budget_tracker)
        return extract_list(q_response)

    generated_questions = 0  # Record the number of generated questions

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while generated_questions < args.number_of_dataset:
            # Calculate the remaining number of questions to generate
            remaining_questions = args.number_of_dataset - generated_questions

            # Generate 50 questions each time, or the remaining number (whichever is smaller)
            batch_size = math.ceil(remaining_questions / 50)

            # Dynamically generate tasks to submit to the thread pool
            future_to_question = {
                executor.submit(process_question, example + topic + conditions): question
                for question in range(batch_size)
            }

            # Iterate over completed tasks
            for future in concurrent.futures.as_completed(future_to_question):
                question = future_to_question[future]
                try:
                    answer = future.result()
                    questions.extend(answer)
                    generated_questions += len(answer)

                    if budget_tracker.is_budget_exceeded():
                        return questions  # Return immediately if the budget is exceeded
                except Exception as e:
                    print(f"Error occurred for question: {question}. Error message: {str(e)}")

            # Check if the desired number of questions has been generated, if so, break the loop
            if generated_questions >= args.number_of_dataset:
                break

    return questions


def generate_subtopic(args: DataSetArguments,
                      budget_tracker: BudgetTracker) -> List[str]:
    # Generate sub-topics based on the given topic, generalization index, generalization basic, API key, and budget
    # tracker
    if args.generalization_basic * args.generalization_index == 0:
        return []

    prompt = f"""
        Generate {int(args.generalization_index * args.generalization_basic)} sub-topics based on the content in the <Topic> tag,
        each sub-topic should have no more than 6 characters,
        wrap each sub-topic with <SubTopic> and </SubTopic> tags
        Here are some examples:
        -- <Topic>When is the Spring Festival coming?</Topic>
           <SubTopic>Year Beast</SubTopic>
           <SubTopic>Red Envelope</SubTopic>
           <SubTopic>Firecrackers</SubTopic>
           <SubTopic>Window Decoration</SubTopic>
           <SubTopic>Spring Couplets</SubTopic>
        -- <Topic>Leo Horoscope</Topic>
           <SubTopic>Pop Culture</SubTopic>
           <SubTopic>Deep Space Objects</SubTopic>
           <SubTopic>Characteristics</SubTopic>
           <SubTopic>Capricorn</SubTopic>
        <Topic>{args.topic}</Topic>
        """
    api = ChatAPI(api_key=args.api_key, proxy=args.proxy)

    return extract_list(api.chat(prompt=prompt, budget_tracker=budget_tracker), 'SubTopic')


def generate_answer(questions: List[str], budget_tracker: BudgetTracker, pbar, args: DataSetArguments):
    # Generate answers for the given list of questions using the API key, budget tracker, progress bar, and output path
    api = ChatAPI(api_key=args.api_key, system_settings='You are a knowledgeable assistant, showcasing your talent!',
                  proxy=args.proxy)
    answers = []

    def process_question(question):
        prompt = f"""
        Answer the following question wrapped in "```". Show off your knowledge,
        but be rigorous like a scholar.
        You can choose not to answer uncertain content
        and answer from a perspective you are familiar with.
        ```
        {question}
        ```
        """
        response = api.chat(prompt=prompt, budget_tracker=budget_tracker)
        answer_dict = {
            "question": question,
            "answer": response
        }
        pbar.update(1)
        return answer_dict

    generated_answers = 0
    current_index = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while generated_answers < len(questions):
            batch_size = min(20, len(questions) - generated_answers)
            questions_batch = questions[current_index:current_index + batch_size]
            current_index = current_index + batch_size
            future_to_question = {executor.submit(process_question, question): question for question in
                                  questions_batch}

            for future in concurrent.futures.as_completed(future_to_question):
                question = future_to_question[future]
                try:
                    answer = future.result()
                    answers.append(answer)
                    generated_answers += 1
                    print((pbar.format_dict['elapsed'] / pbar.n) * (pbar.total - pbar.n))
                    log_dict = {
                        "current_number": pbar.n,
                        "total_count": pbar.total,
                        "percentage": pbar.n / pbar.total,
                        "elapsed_time": str(timedelta(seconds=int(pbar.format_dict['elapsed']))),
                        "remaining_time": str(timedelta(seconds=int((pbar.format_dict['elapsed'] / pbar.n) * (pbar.total - pbar.n)))),
                        "budget": budget_tracker.total_budget,
                        "current_cost": budget_tracker.current_cost
                    }
                    print(json.dumps(log_dict))
                    if budget_tracker.is_budget_exceeded() or pbar.n == pbar.total:
                        write_dict_list_to_file(data_list=answers, output_path=args.dataset_output_path)
                        sys.exit(0)
                except Exception as e:
                    print(f"Error occurred for question: {question}. Error message: {str(e)}")

    write_dict_list_to_file(data_list=answers, output_path=args.dataset_output_path)
