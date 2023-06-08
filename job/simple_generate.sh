#!/bin/bash

# 泛化数值
generalization_index=$1
# 主题
topic=$2
# OpenAI Key
api_key=$3
# 数据集保存路径
dataset_output_path=$4

python src/main.py \
--generalization_index ${generalization_index} \
--topic ${topic} \
--api_key ${api_key} \
--dataset_output_path ${dataset_output_path}