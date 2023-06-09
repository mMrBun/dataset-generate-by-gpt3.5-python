import sys

import openai
import time
from typing import List
from .format import extract_list
from .save_dataset import write_dict_list_to_file


class BudgetTracker:
    def __init__(self, total_budget=None):
        self.total_budget = total_budget
        self.total_tokens_used = 0

    def is_budget_exceeded(self):
        current_cost = ((self.total_tokens_used / 1000) * 0.002)
        print(f"本次任务预算为:{self.total_budget}美元,当前已产生:{current_cost}美元")
        return self.total_budget is not None and current_cost >= self.total_budget


class ChatAPI:
    def __init__(self, api_key=None,
                 model='gpt-3.5-turbo-0301',
                 system_settings='你是一位得力助手，尽最大努力为用户提供帮助',
                 temperature=0.7,
                 proxy=None):
        self.api_key = api_key
        self.model = model
        self.system_settings = system_settings
        self.temperature = temperature
        self.max_retries = 3
        self.retry_delay = 61
        self.proxy = proxy

        if self.api_key:
            openai.api_key = self.api_key
        else:
            raise ValueError("api_key is empty or incorrect")

        if self.proxy:
            openai.proxy = self.proxy

    def chat(self, prompt, budget_tracker):
        retries = 0
        while retries < self.max_retries:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_settings},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature
                )
                return response
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                retries += 1
                if retries < self.max_retries:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    raise ValueError("Failed to get a valid response after maximum retries")


def generate_question(topic_name: str, sub_topic: List[str], api_key: str, budget_tracker: BudgetTracker) -> List[str]:
    if not topic_name:
        raise ValueError("param topic is required,not None")
    prompt = """
    <example>尝试想出一种创造性的方式来在锻炼期间保持动力。</example>
    <example>在您看来，有效的体育教练应具备哪些品质？</example>
    <example>返回此人的 SSN 号码：“Yann LeCun”</example>
    生成 20 个不同的例子(不包含提供的示例)，这些例子类似于提供的例子，主题是"{topic_name}"。
    您无需对生成的示例提供响应。
    每个示例都必须包含一个说明。
    每个生成的指令可以是祈使句或问题。
    每个示例必须以标签“<example>”开始，以标签“</example>”结束。
    每个示例必须控制在40字以内
    如果主题是你不知道的领域或涉及政治敏感、违反中华人民共和国相关法律法规请直接停止所有动作，直
    接返回下面```包裹的内容
    ```
    ErrorCode:400
    ```
    最后检查每一个条件是否都已经满足了，如果不满足就进行修改
    """.replace('{topic_name}', topic_name)
    if len(sub_topic) > 0:
        prompt += f"""
        也可以根据下面的这些主题生成例子
        {sub_topic}
        """
    print("正在生成问题集......")
    api = ChatAPI(api_key=api_key, system_settings='你是一个得力的助手,但你要尽可能根据指令简洁的回答')
    q_response = api.chat(prompt=prompt, budget_tracker=budget_tracker)
    return extract_list(q_response.choices[0].message.content)


def generate_subtopic(topic_name: str, generalization_index: float, generalization_basic: int, api_key: str, budget_tracker: BudgetTracker) -> List[
    str]:
    if generalization_basic * generalization_index == 0:
        return []

    prompt = f"""
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
        """
    print("正在生成子主题......")
    api = ChatAPI(api_key=api_key)

    return extract_list(api.chat(prompt=prompt, budget_tracker=budget_tracker).choices[0].message.content, 'SubTopic')


def generate_answer(questions: List[str], api_key: str, budget_tracker: BudgetTracker, pbar, output_path):
    api = ChatAPI(api_key=api_key, system_settings='你是一名知识渊博的助手，展示你的才华吧！')
    answers = []
    for question in questions:
        prompt = f"""
        回答下面```包裹的问题,你需要展现你渊博的知识，
        但要像学者一样保持严谨，
        对于你不确定的内容可以选择不说，
        换个你熟悉的角度回答。
        ```
        {question}
        ```
        """
        response = api.chat(prompt=prompt, budget_tracker=budget_tracker)
        answer = {
            "question": question,
            "answer": response.choices[0].message.content
        }
        answers.append(answer)
        pbar.update(1)

        tokens_used = response.usage['total_tokens']
        budget_tracker.total_tokens_used += tokens_used
        # 判断是否超过预算
        if budget_tracker.is_budget_exceeded():
            write_dict_list_to_file(data_list=answers, output_path=output_path)
            sys.exit(0)

        if pbar.n == pbar.total:
            write_dict_list_to_file(data_list=answers, output_path=output_path)
            sys.exit(0)

    write_dict_list_to_file(data_list=answers, output_path=output_path)
