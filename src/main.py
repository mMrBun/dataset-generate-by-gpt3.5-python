import json
import argparse

from utils import (
    generate_subtopic,
    generate_question
)

parser = argparse.ArgumentParser()
parser.add_argument('--generalization_index', type=float, default=0, help='泛化指数,越高数据集的多样性更丰富')
parser.add_argument('--generalization_basic', type=int, default=10, help='比例系数,即y=kx+b中的k')
parser.add_argument('--topic', type=str, default=None, help='数据集主题')
parser.add_argument('--api_key', type=str, default=None, help='OpenAI API KEY')
args = parser.parse_args()


def main():

    sub_topic = generate_subtopic(topic_name=args.topic, generalization_index=args.generalization_index,
                                  generalization_basic=args.generalization_basic, api_key=args.api_key)
    response = generate_question(topic_name=args.topic, subTopic=sub_topic, api_key=args.api_key)
    for item in response:
        question_dict = {
            'instruction': item,
            'input': ''
        }
        with open("../data/q_a_pair.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(question_dict, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
