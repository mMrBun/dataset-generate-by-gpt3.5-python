#!/bin/bash

python src/main.py \
--generalization_index 0.75 \
--generalization_basic 10 \
----number_of_dataset 500 \
--topic 螃蟹为什么横着走路 \
--api_key sk-xxxxx \
--proxy http://127.0.0.1:7890 \
--tokenBudget 5 \
--dataset_output_path data