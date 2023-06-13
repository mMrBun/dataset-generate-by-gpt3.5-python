# 数据集生成

[//]: # (![GitHub Repo stars]&#40;https://img.shields.io/github/stars/mMrBun/DatasetGenerate?style=social&#41;)
[![License: GPL v3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

- 支持接口retry
- 新增生成数据集进度条
- 支持预算控制


用OpenAI GPT3.5 API根据所提供主题生成相关领域的数据集

受到[LaMini](https://github.com/mbzuai-nlp/LaMini-LM) 的论文启发写了这个项目，原文中的方式为爬取维基百科中的词条，经过删选条件筛选出符合条件的词条以及关联词条，之后使用下面的prompt对gpt3.5
进行询问

~~~ json
<example>Try coming up with a creative way to stay motivated during a workout.</example>
<example>In your opinion, what are the qualities of an effective sports coach?</example>
<example>Return the SSN number for the person: "Yann LeCun"</example>
Generate 20 diverse examples that are similar to the provided examples with the topics "Design
,→ bureaus, Conidae, Infantry".
You do not need to provide a response to the generated examples.
Each example must include an instruction.
Each generated instruction can be either an imperative sentence or a question.
Each example must start with the label "<example>" and end with the label "</example>".".
~~~

将得到的问题再次抛给gpt3.5得到回答，这就算一条数据，之后重复上述步骤就可以得到一个通识类的数据集。

我稍微改变了一下主题引导式生成的方式，根据输入的一个主题使用下面的prompt得到相关的子主题，之后通过上述步骤完成数据集构建
~~~ json
以<Topic>标签中的内容为主题生成{int(generalization_index * generalization_basic)}个子主题,
        每个子主题字数不超过6个字,
        以<SubTopic>开始,以</SubTopic>结束包裹每个子主题
        以下是一些列子
        -- <Topic>春节什么时候来啊？</Topic>
           <SubTopic>年兽</SubTopic>
           <SubTopic>红包</SubTopic>
           <SubTopic>放鞭炮</SubTopic>
           <SubTopic>贴窗花</SubTopic>
           <SubTopic>贴春联</SubTopic>
        -- <Topic>狮子座运势</Topic>
           <SubTopic>流行文化</SubTopic>
           <SubTopic>深空天体</SubTopic>
           <SubTopic>特征</SubTopic>
           <SubTopic>魔羯座</SubTopic>
        <Topic>{topic_name}</Topic>
~~~


## 快速开始

参数详情请参阅[WIKI](https://github.com/mMrBun/DatasetGenerate/wiki)
### Linux
~~~ sybase
conda create -n dataset_generate python=3.8

conda activate dataset_generate

git clone https://github.com/mMrBun/DatasetGenerate.git

cd DatasetGenerate

pip install -r requirments.txt 

sudo chmod +x job/simple_generate.sh

job/simple_generate.sh
~~~

### Windows
在参数栏中填写必要参数
![img.png](img/img.png)
~~~ sybase
--topic 螃蟹为什么横着走路 --api_key sk-xxx --number_of_dataset 100
~~~
