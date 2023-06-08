import openai
import time
from typing import List
from .format import extract_list


class ChatAPI:
    def __init__(self, api_key=None,
                 model='gpt-3.5-turbo',
                 system_settings='你是一位得力助手，尽最大努力为用户提供帮助',
                 temperature=0.7):
        self.api_key = api_key
        self.model = model
        self.system_settings = system_settings
        self.temperature = temperature
        self.max_retries = 3
        self.retry_delay = 61

        if self.api_key:
            openai.api_key = self.api_key
        else:
            raise ValueError("api_key is empty or incorrect")

        # openai.proxy = 'http://127.0.0.1:7890'

    def chat(self, prompt):
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
                return response.choices[0].message.content
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                retries += 1
                if retries < self.max_retries:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    raise ValueError("Failed to get a valid response after maximum retries")


def generate_question(topic_name: str, subTopic: List[str], api_key: str) -> List[str]:
    prompt = """
    <example>尝试想出一种创造性的方式来在锻炼期间保持动力。</example>
    <example>在您看来，有效的体育教练应具备哪些品质？</example>
    <example>返回此人的 SSN 号码：“Yann LeCun”</example>
    生成 50 个不同的例子，这些例子类似于提供的例子，主题是"{topic_name}"。
    您无需对生成的示例提供响应。
    每个示例都必须包含一个说明。
    每个生成的指令可以是祈使句或问题。
    每个示例必须以标签“<example>”开始，以标签“</example>”结束。
    每个示例必须控制在50字以内
    如果主题是你不知道的领域或涉及政治敏感、违反中华人民共和国相关法律法规请直接停止所有动作，直
    接返回下面```包裹的json
    ```
    {
        "error": {
            "message": "主题不符合本平台规范，请修改后重试，三次违规账号将被冻结",
            "type": "invalid_request_error",
            "param": null,
            "code": "invalid_topic"
        }
    }
    ```
    最后检查每一个条件是否都已经满足了，如果不满足就进行修改
    """.replace('{topic_name}', topic_name)
    if len(subTopic) > 0:
        prompt += f"""
        也可以根据下面的这些主题生成例子
        {subTopic}
        """
    api = ChatAPI(api_key=api_key, system_settings='你是一个得力的助手,但你要尽可能根据指令简洁的回答')
    q_response = api.chat(prompt=prompt)
    return extract_list(q_response)


def generate_subtopic(topic_name: str, generalization_index: float, generalization_basic: int, api_key: str):
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
    api = ChatAPI(api_key=api_key)

    return extract_list(api.chat(prompt=prompt), 'SubTopic')
