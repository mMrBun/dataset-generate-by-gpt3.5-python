import re
from argparse import ArgumentParser
from dataclasses import dataclass, field


def extract_list(answers, tag='example'):
    if "ErrorCode:400" in answers:
        raise ValueError("主题不符合本平台规范，请修改后重试，三次违规账号将被冻结")
    pattern = rf"<{tag}>(.*?)</{tag}>"
    texts = re.findall(pattern, answers, re.DOTALL)
    return texts


@dataclass
class DataSetArguments:
    generalization_index: float = field(
        default=0.0,
        metadata={"help": "Generalization Index, the higher it is, the more diverse the dataset is. Default value is "
                          "0.0"}
    )

    generalization_basic: int = field(
        default=10,
        metadata={"help": "The scaling factor, represented by k in the equation y = kx + b. Default value is 10"}
    )

    number_of_dataset: int = field(
        default=500,
        metadata={"help": "The number of generated dataset. Default is 500"}
    )

    topic: str = field(
        default=None,
        metadata={"Help": "Dataset topics. Default is None"}
    )

    dataset_output_path: str = field(
        default='data',
        metadata={"Help": "Path to save dataset"}
    )

    proxy: str = field(
        default=None,
        metadata={
            "Help": "If you are unable to access OpenAI, please provide a proxy address. eg:http://127.0.0.1:7890"}
    )

    api_key: str = field(
        default=None,
        metadata={"Help": "The OpenAI API-KEY"}
    )

    tokenBudget: float = field(
        default=1,
        metadata={"Help": "Dataset topics. Default is None"}
    )


def prepare_args() -> DataSetArguments:
    parser = ArgumentParser()
    parser.add_argument('--generalization_index', type=float, default=0.0)
    parser.add_argument('--generalization_basic', type=int, default=10)
    parser.add_argument('--number_of_dataset', type=int, default=100)
    parser.add_argument('--topic', type=str, default=None)
    parser.add_argument('--dataset_output_path', type=str, default='data')
    parser.add_argument('--proxy', type=str, default=None)
    parser.add_argument('--api_key', type=str, default=None)
    parser.add_argument('--tokenBudget', type=float, default=1)
    args = parser.parse_args()
    model_args = DataSetArguments(
        generalization_index=args.generalization_index,
        generalization_basic=args.generalization_basic,
        number_of_dataset=args.number_of_dataset,
        topic=args.topic,
        dataset_output_path=args.dataset_output_path,
        proxy=args.proxy,
        api_key=args.api_key,
        tokenBudget=args.tokenBudget
    )
    return model_args
