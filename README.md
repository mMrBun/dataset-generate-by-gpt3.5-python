# DatasetGenerate

[//]: # (![GitHub Repo stars]&#40;https://img.shields.io/github/stars/mMrBun/DatasetGenerate?style=social&#41;)
[![License: GPL v3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Generate a dataset in a subject-related field using the OpenAI GPT-3.5 API.


\[ English | [中文](README_zh.md) \]

## Requirements
- You only need an OpenAI API key to generate a dataset in a relevant subject. The generalization factor and the number of generations can be customized.
- By default, there is no proxy. If you need to use a proxy, please uncomment line 24 in `src/utils/gpt_api.py` and modify it accordingly.

## Quick Start
### Linux
```shell
conda create -n dataset_generate python=3.8

conda activate dataset_generate

git clone https://github.com/mMrBun/DatasetGenerate.git

cd DatasetGenerate

pip install -r requirements.txt

sudo chmod +x job/simple_generate.sh

job/simple_generate.sh $1 $2 $3 $4
```

### Windows
```shell
conda create -n dataset_generate python=3.8

activate dataset_generate

git clone https://github.com/mMrBun/DatasetGenerate.git

cd DatasetGenerate

pip install -r requirements.txt

job/simple_generate.bat $1 $2 $3 $4
```

## TODO

- [ ] Support specifying a budget and automatically stopping when exceeded.
- [ ] Add a logging system to print progress, process parameters, and real-time cost to a local file.