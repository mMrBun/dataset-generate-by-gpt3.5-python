from tqdm.auto import tqdm
from utils import (
    generate_subtopic,
    generate_question,
    generate_answer,
    prepare_args,
    BudgetTracker
)

args = prepare_args()


def main():
    # Create a budget tracker to keep track of the token budget
    budget_tracker = BudgetTracker(total_budget=args.tokenBudget)

    # Initialize a progress bar with the total number of datasets to be generated
    pbar = tqdm(total=args.number_of_dataset, desc="Processing")

    while pbar.n < pbar.total:
        # Generate a subtopic based on the provided topic and generalization parameters
        sub_topic = generate_subtopic(topic_name=args.topic,
                                      generalization_index=args.generalization_index,
                                      generalization_basic=args.generalization_basic,
                                      api_key=args.api_key,
                                      budget_tracker=budget_tracker)

        # Generate questions based on the topic, subtopic, and API key
        questions = generate_question(topic_name=args.topic,
                                      sub_topic=sub_topic,
                                      api_key=args.api_key,
                                      budget_tracker=budget_tracker,
                                      number_of_dataset=args.number_of_dataset)

        # Generate answers for the questions using the API key and update the budget tracker and progress bar
        generate_answer(questions=questions,
                        api_key=args.api_key,
                        budget_tracker=budget_tracker,
                        pbar=pbar,
                        output_path=args.dataset_output_path)


if __name__ == '__main__':
    main()
