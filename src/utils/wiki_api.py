import requests
import wikipediaapi
from bs4 import BeautifulSoup


def get_wikipedia_categories(topic_name):
    # 构建搜索链接
    search_url = f"https://zh.wikipedia.org/w/index.php?search={topic_name}&title=Special:%E6%90%9C%E7%B4%A2&profile" \
                 f"=advanced&fulltext=1&ns0=1"

    # 发送请求并获取页面内容
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 获取搜索结果中的条目数量
    result_info = soup.find('div', class_='mw-pager-navigation-bar')
    if result_info:
        result_count = result_info.find_all('a', class_='mw-numlink')[-1]
        result_count = int(result_count.text)

        # 判断是否满足条件
        if result_count >= 50:
            return search_wikipedia(topic_name)

    return []


def search_wikipedia(topic_name):
    # 存储符合条件的相关类别
    related_categories = []

    # 创建维基百科API对象
    wiki_api = wikipediaapi.Wikipedia('zh')

    # 获取主题页面
    page = wiki_api.page(topic_name)

    # 检查主题是否存在
    if page.exists():
        if len(page.backlinks) > 10:
            section = page.sections
            for item in section:
                for i in item.sections:
                    related_categories.append(i.title)

    return related_categories


# 测试示例
topic = input("请输入主题：")
categories = get_wikipedia_categories(topic)

if categories:
    print("符合条件的相关类别：")
    for category in categories:
        print(category)
else:
    print("未找到符合条件的相关类别。")
