import os
import json


def write_dict_list_to_file(data_list, output_path):
    # Create the directory at the specified output path if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    # Create the file path for the dataset file
    file_path = os.path.join(output_path, "dataset.jsonl")
    # Open the file in append mode and use UTF-8 encoding
    with open(file_path, "a", encoding="utf-8") as f:
        for item in data_list:
            question_dict = {
                'instruction': item["question"],
                'input': '',
                'output': item["answer"]
            }
            f.write(json.dumps(question_dict, ensure_ascii=False) + '\n')


def log_generating_params(log_dict):
    print(log_dict)
