import re


def extract_list(answers, tag='example'):
    pattern = rf"<{tag}>(.*?)</{tag}>"
    texts = re.findall(pattern, answers, re.DOTALL)
    return texts
