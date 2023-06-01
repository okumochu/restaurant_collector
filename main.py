from spider import scrape_comments
from countToken import *
from chatgpt import summary
from ft_restaurant import get_restaurant_urls
from dotenv import load_dotenv
import os
from multiprocessing import Pool
from functools import partial


def mutiprocess_task(url_list, focus_point):
    list_comments = []
    restaurant_name = []
    print("start scaping comments")
    contents, name = scrape_comments(url_list)
    restaurant_name.append(name)
    list_comments.append(contents)
    print(name)
    print(contents)

    load_dotenv()

    for comments, name in zip(list_comments, restaurant_name):
        print('start comments->gpt format')
        message, index = article_to_GPT(comments, 0)
        print('start gpt->summary')
        # print(focus_point)
        summary(name, message=message, focus_point=focus_point,
                api_key=os.getenv("openai_api_key"))


if __name__ == '__main__':
    focus_point = input('請問您在意的點是什麼： ')
    url_list = get_restaurant_urls(int(input('你要搜尋幾間餐廳: ')))
    print(len(url_list))
    pool = Pool(processes=3)
    partial_func = partial(mutiprocess_task, focus_point=focus_point)
    pool.map(partial_func, url_list)
    pool.close()
    pool.join()
    os.rename('output.txt', 'output.md')


# url_list = get_restaurant_urls(1)
# print(len(url_list))
# list_comments = []
# restaurant_name = []
# for url in url_list:
#     print("start scaping comments")
#     conents, name = scrape_comments(url)
#     restaurant_name.append(name)
#     list_comments.append(conents)
#     print(name)
#     print(conents)

# load_dotenv()

# for comments, name in zip(list_comments, restaurant_name):
#     print('start comments->gpt format')
#     message, index = article_to_GPT(comments, 0)
#     print('start gpt->summary')
#     summary(name, message=message, api_key=os.getenv("openai_api_key"))
