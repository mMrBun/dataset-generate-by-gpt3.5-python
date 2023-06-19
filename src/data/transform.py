import json

new_data = []
with open('dataset.jsonl', 'rb') as file:
    for line in file:
        decoded_line = line.decode('utf-8')
        new_data.append(json.loads(decoded_line))

new_data_json = json.dumps(new_data, ensure_ascii=False, indent=4)  # 设置缩进为4个空格

# 保存为新的文件
with open('new_data.json', 'w', encoding='utf-8') as outfile:
    outfile.write(new_data_json)
