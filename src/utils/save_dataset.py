import os
import json


def write_dict_list_to_file(data_list, output_path):
    os.makedirs(output_path, exist_ok=True)
    file_path = os.path.join(output_path, "dataset.jsonl")
    with open(file_path, "a", encoding="utf-8") as f:
        for item in data_list:
            question_dict = {
                'instruction': item["question"],
                'input': '',
                'output': item["answer"]
            }
            f.write(json.dumps(question_dict, ensure_ascii=False) + '\n')
