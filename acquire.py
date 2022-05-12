import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Acquire Codeup Blog Articles

def get_blog_article_urls():
    headers = {'user-agent': 'Innis Codeup Data Science'}
    response = requests.get('https://codeup.com/blog/', headers=headers)
    soup = BeautifulSoup(response.text)
    urls = [a.attrs['href'] for a in soup.select('a.more-link')]
    return urls

def parse_blog_article(soup):
    return {
        'title': soup.select_one('h1.entry-title').text,
        'published': soup.select_one('.published').text,
        'content': soup.select_one('.entry-content').text.strip(),
    }

def get_codeup_articles(use_cache=True):
    if os.path.exists('codeup_blog_articles.json') and use_cache:
        return pd.read_json('codeup_blog_articles.json')

    urls = get_blog_article_urls()
    headers = {'user-agent': 'Innis Codeup Data Science'}
    articles = []

    for url in urls:
        print(f'fetching {url}')
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text)
        articles.append(parse_blog_article(soup))

    df = pd.DataFrame(articles)
    df.to_json('codeup_blog_articles.json', orient='records')
    return 


# Acquire InShorts Articles

def parse_news_card(card, category):
    '''
    Take in a news card and generate a dictionary
    '''
    output = {}
    output['category'] = category
    output['title'] = card.select_one('a.clickable').text.strip()
    
    cards = card.select_one('div.news-card')
    output['content'] = card.select_one('div.news-card-content').text.strip()
    output['author'] = card.select_one('.author').text
    output['published'] = card.select_one('.time').attrs['content']
    return output

def parse_inshorts_page(category): 
    '''
    
    '''
    url = 'https://www.inshorts.com/en/read/'+ category
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    articles = [parse_news_card(card, category) for card in soup.select('.news-card')]
    return articles

def get_inshorts_articles():
    '''
    Combine all articles from multiple categories into one data frame
    '''
    categories = ['business', 'sports', 'entertainment', 'technology']
    articles = []
    
    for category in categories:
        print(f'Getting articles for {category}')
        category_articles = parse_inshorts_page(category)
        articles.extend(category_articles) 
    df=pd.DataFrame(articles)
    df.to_json('news_articles.json', orient='records')
    return df