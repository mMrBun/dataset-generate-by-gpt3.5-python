import json

from utils import (
    extract_list,
    chat
)


def generate_question(topic, subTopic):
    prompt = f"""
    <example>尝试想出一种创造性的方式来在锻炼期间保持动力。</example>
    <example>在您看来，有效的体育教练应具备哪些品质？</example>
    <example>返回此人的 SSN 号码：“Yann LeCun”</example>
    生成 50 个不同的例子，这些例子类似于提供的例子，主题是"{topic}"。
    您无需对生成的示例提供响应。
    每个示例都必须包含一个说明。
    每个生成的指令可以是祈使句或问题。
    每个示例必须以标签“<example>”开始，以标签“</example>”结束。
    每个示例必须控制在70字以内
    """
    if len(subTopic) > 0:
        prompt += f"""
        也可以根据下面的这些主题生成例子
        {subTopic}
        """
    response = chat(prompt=prompt, system_settings='你是一个得力的助手,但你要尽可能根据指令简洁的回答')
    return extract_list(response)


def generate_subtopic(topic_name, generalization_index, generalization_basic):
    prompt = f"""
        以<Topic>标签中的内容为主题生成{int(generalization_basic * generalization_index)}个子主题,
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
    return extract_list(chat(prompt), 'SubTopic')


if __name__ == '__main__':
    generalization_index = 0.75

    generalization_basic = 10

    topic = "狮子座运势"

    sub_topic = generate_subtopic(topic_name=topic, generalization_index=generalization_index,
                                  generalization_basic=generalization_basic)
    response = generate_question(topic=topic, subTopic=sub_topic)
    for item in response:
        question_dict = {
            'instruction': item,
            'input': ''
        }
        with open("q_a_pair.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(question_dict, ensure_ascii=False) + '\n')
