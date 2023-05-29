from countToken import article_to_GPT
from spider import scrape_comments
from chatgpt import summary
from ft_restaurant import get_restaurant_urls
from dotenv import load_dotenv
import os
import markdown
# Only for the article that splits lines


with open('output.txt', 'a', encoding='utf-8') as output_file:
    output_file.write('# name')
    output_file.write('\n')
    output_file.write('# name')
