# 数据集生成

[//]: # (![GitHub Repo stars]&#40;https://img.shields.io/github/stars/mMrBun/DatasetGenerate?style=social&#41;)
[![License: GPL v3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

用OpenAI GPT3.5接口生成所提供主题相关领域的数据集

## 需求条件
- 你只需要一个OpenAI APIKey就可以生成相关主题的数据集，泛化指数以及生成数量都支持自定义。
- 默认没有代理，如果需要代理请解除并修改 src/utils/gpt_api.py 24行的注释
## 快速开始
### Linux
~~~ sybase
conda create -n dataset_generate python=3.8

conda activate dataset_generate

git clone https://github.com/mMrBun/DatasetGenerate.git

cd DatasetGenerate

pip install -r requirments.txt 

sudo chmod +x job/simple_generate.sh

job/simple_generate.sh $1 $2 $3 $4
~~~
### Windows
~~~ sybase
conda create -n dataset_generate python=3.8

activate dataset_generate

git clone https://github.com/mMrBun/DatasetGenerate.git

cd DatasetGenerate

pip install -r requirments.txt 

job/simple_generate.bat $1 $2 $3 $4
~~~ 

## TODO

- [ ] 支持指定预算，超过预算自动停止
- [ ] 增加日志系统，终端打印进度，过程参数，费用实时写入本地文件
