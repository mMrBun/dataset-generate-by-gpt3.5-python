from utils import (
    extract_list,
    chat
)


def main(topic, subTopic):
    """
    <example>尝试想出一种创造性的方式来在锻炼期间保持动力。</example>
    <example>在您看来，有效的体育教练应具备哪些品质？</example>
    <example>返回此人的 SSN 号码：“Yann LeCun”</example>
    生成 20 个不同的例子，这些例子类似于提供的例子，主题是“”。
    您无需对生成的示例提供响应。
    每个示例都必须包含一个说明。
    每个生成的指令可以是祈使句或问题。
    每个示例必须以标签“<example>”开始，以标签“</example>”结束。
    每个示例必须控制在70字以内
    :param topic:
    :return:
    """
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
    chat(prompt=prompt, system_settings='你是一个得力的助手,但你要尽可能根据指令简洁的回答')

#     generate_question_prompt = ""
#     for item in topic:
#         generate_question_prompt += f"<example>{item}</example>"
#     generate_question_prompt += f"""
#         生成 50 个与提供的示例相似的不同示例。
#         您无需对生成的示例提供响应。
#         每个示例都必须包含一个说明。
#         每个生成的指令可以是祈使句或问题。
#         每个示例必须以标签“<example>”开始，以标签“</example>”结束。
#         每个示例必须控制在70字以内
#         """
#     tools = OpenAI_Tools()
#     answer = tools.generate_question_by_little_example(generate_question_prompt)
#     questions = answer_2_list(answer)
#     for question in questions:
#         generate_answer_prompt = f"""
#             {question}
#             """
#         target = tools.send_request(generate_answer_prompt)
#         q_a_pair = {
#             "instruction": question,
#             "output": target.choices[0].message.content
#         }
#         with open("q_a_pair.jsonl", "a", encoding="utf-8") as f:
#             f.write(json.dumps(q_a_pair, ensure_ascii=False) + '\n')
#
#
# if __name__ == '__main__':
#     example_list = {
#         "天秤座是什么样的性格？",
#         "告诉我天秤座和什么星座性格最合得来"
#     }
#     main(example_list)
