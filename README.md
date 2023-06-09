# DatasetGenerate

[//]: # (![GitHub Repo stars]&#40;https://img.shields.io/github/stars/mMrBun/DatasetGenerate?style=social&#41;)
[![License: GPL v3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Generate a dataset in a subject-related field using the OpenAI GPT-3.5 API.


\[ English | [中文](README_zh.md) \]

## Quick Start
### Linux
```shell
conda create -n dataset_generate python=3.8

conda activate dataset_generate

git clone https://github.com/mMrBun/DatasetGenerate.git

cd DatasetGenerate

pip install -r requirements.txt

sudo chmod +x job/simple_generate.sh

job/simple_generate.sh
```