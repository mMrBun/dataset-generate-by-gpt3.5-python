import json
import os
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
    """
    基本流程梳理
    - 生成数量控制
    - 如果泛化指数和基数乘积为零则不调用子主题函数
    - 生成问题
    - 生成答案
    - 写文件
    :return:
    """
    # for turn in range(args.number_of_dataset // 50):
    budget_tracker = BudgetTracker(total_budget=args.tokenBudget)
    pbar = tqdm(total=args.number_of_dataset, desc="Processing")
    while pbar.n < pbar.total:
        sub_topic = generate_subtopic(topic_name=args.topic,
                                      generalization_index=args.generalization_index,
                                      generalization_basic=args.generalization_basic,
                                      api_key=args.api_key,
                                      budget_tracker=budget_tracker)

        questions = generate_question(topic_name=args.topic,
                                      subTopic=sub_topic,
                                      api_key=args.api_key,
                                      budget_tracker=budget_tracker)

        answers = generate_answer(questions=questions,
                                  api_key=args.api_key,
                                  budget_tracker=budget_tracker,
                                  pbar=pbar)

        for item in answers:
            question_dict = {
                'instruction': item["question"],
                'input': '',
                'output': item["answer"]
            }
            os.makedirs(args.dataset_output_path, exist_ok=True)
            with open(os.path.join(args.dataset_output_path, "dataset.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps(question_dict, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
