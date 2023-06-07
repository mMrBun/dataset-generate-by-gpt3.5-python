import openai

openai.api_key = 'xxxxxxxxx'


def chat(prompt, model='gpt-3.5-turbo', system_settings='你是一位得力助手,尽最大努力为用户提供帮助', temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_settings},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content


if __name__ == '__main__':

    # 泛化指数
    generalization_index = 0.75

    # 泛化基数
    generalization_basic = 10

    # 主题
    topic = "狮子座运势"

    prompt = f"""
    以<Topic>标签中的内容为主题生成{int(generalization_basic*generalization_index)}个子主题,
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
    <Topic>{topic}</Topic>
    """

    print(chat(prompt))
