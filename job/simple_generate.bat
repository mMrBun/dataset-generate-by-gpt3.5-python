@echo off

set generalization_index=%1
set topic=%2
set api_key=%3
set dataset_output_path=%4

python src/main.py ^
--generalization_index %generalization_index% ^
--topic %topic% ^
--api_key %api_key% ^
--dataset_output_path %dataset_output_path%


