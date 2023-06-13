import math
import concurrent.futures
import random
import sys

import openai
import time
from typing import List
from .format import extract_list
from .save_dataset import write_dict_list_to_file


class BudgetTracker:
    def __init__(self, total_budget=None):
        self.total_budget = total_budget
        self.total_tokens_used = 0

    def is_budget_exceeded(self):
        current_cost = ((self.total_tokens_used / 1000) * 0.002)
        print(f"本次任务预算为:{self.total_budget}美元,当前已产生:{current_cost}美元")
        return self.total_budget is not None and current_cost >= self.total_budget


class ChatAPI:
    def __init__(self, api_key=None,
                 model='gpt-3.5-turbo-0301',
                 system_settings='你是一位得力助手，尽最大努力为用户提供帮助',
                 temperature=0.7,
                 proxy=None):
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


def generate_question(topic_name: str, sub_topic: List[str], api_key: List[str], budget_tracker: BudgetTracker,
                      number_of_dataset: int) -> List[str]:
    if not topic_name:
        raise ValueError("param topic is required, not None")

    example = """
    <example>螃蟹为什么横着走比直着走更适合在水中行动？</example>
    <example>请列举出中国四大名著的作者，发行时间以及连载年数</example>
    """

    topic = ""
    if len(sub_topic) > 0:
        topic += f"""
           请以{topic_name, sub_topic}为主题生成50个上述<example>中类似的示例
           """
    else:
        topic = f"""
           请以{topic_name}为主题生成50个上述<example>中类似的示例
           """

    conditions = """
    您无需对生成的示例回答或解释
    每个生成的指令必须是祈使句或疑问句
    祈使句和疑问句的生成比例是1:1
    每个示例必须以标签“<example>”开始，以标签“</example>”结束
    每个示例必须控制在40字以内
    如果主题是你不知道的领域或涉及政治敏感、违反中华人民共和国相关法律法规请直接停止所有动作，直
    接返回下面```包裹的内容
    ```
    ErrorCode:400
    ```
    """
    questions = []

    def process_question(prompt):
        api = ChatAPI(api_key=api_key, system_settings='你是一名得力助手，根据指令尽可能简洁的回答问题')
        q_response = api.chat(prompt=prompt, budget_tracker=budget_tracker)
        return extract_list(q_response)

    generated_questions = 0  # 记录已生成的问题数量

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while generated_questions < number_of_dataset:
            # 计算剩余需要生成的问题数量
            remaining_questions = number_of_dataset - generated_questions

            # 每次生成50个问题，或者剩余数量（以较小的值为准）
            batch_size = math.ceil(remaining_questions / 50)

            # 动态生成要提交给线程池的任务
            future_to_question = {
                executor.submit(process_question, example + topic + conditions): question
                for question in range(batch_size)
            }

            # 遍历已完成的任务
            for future in concurrent.futures.as_completed(future_to_question):
                question = future_to_question[future]
                try:
                    answer = future.result()
                    questions.extend(answer)
                    generated_questions += len(answer)

                    if budget_tracker.is_budget_exceeded():
                        return questions  # 超过预算则立即返回
                except Exception as e:
                    print(f"Error occurred for question: {question}. Error message: {str(e)}")

            # 判断是否满足生成数量的要求，若满足则跳出循环
            if generated_questions >= number_of_dataset:
                break

    return questions


def generate_subtopic(topic_name: str, generalization_index: float, generalization_basic: int, api_key: List[str],
                      budget_tracker: BudgetTracker) -> List[
    str]:
    if generalization_basic * generalization_index == 0:
        return []

    prompt = f"""
        以<Topic>标签中的内容为主题生成{int(generalization_index * generalization_basic)}个子主题,
        每个子主题字数不超过6个字,
        以<SubTopic>开始,以</SubTopic>结束包裹每个子主题
        以下是一些列子
        -- <Topic>春节什么时候来啊？</Topic>
           <SubTopic>年兽</SubTopic>
           <SubTopic>红包</SubTopic>
           <SubTopic>放鞭炮</SubTopic>
           <SubTopic>贴窗花</SubTopic>
           <SubTopic>贴春联</SubTopic>
        -- <Topic>狮子座运势</Topic>
           <SubTopic>流行文化</SubTopic>
           <SubTopic>深空天体</SubTopic>
           <SubTopic>特征</SubTopic>
           <SubTopic>魔羯座</SubTopic>
        <Topic>{topic_name}</Topic>
        """
    print("正在生成子主题......")
    api = ChatAPI(api_key=api_key)

    return extract_list(api.chat(prompt=prompt, budget_tracker=budget_tracker), 'SubTopic')


def generate_answer(questions: List[str], api_key: List[str], budget_tracker: BudgetTracker, pbar, output_path):
    api = ChatAPI(api_key=api_key, system_settings='你是一名知识渊博的助手，展示你的才华吧！')
    answers = []

    def process_question(question):
        prompt = f"""
        回答下面```包裹的问题,你需要展现你渊博的知识，
        但要像学者一样保持严谨，
        对于你不确定的内容可以选择不说，
        换个你熟悉的角度回答。
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
                    if budget_tracker.is_budget_exceeded() or pbar.n == pbar.total:
                        write_dict_list_to_file(data_list=answers, output_path=output_path)
                        sys.exit(0)
                except Exception as e:
                    print(f"Error occurred for question: {question}. Error message: {str(e)}")

    write_dict_list_to_file(data_list=answers, output_path=output_path)
