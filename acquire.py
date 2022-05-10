import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Acquire Codeup Blog Articles

def get_front_page_links():
    """
    Short function to hit the codeup blog landing page and return a list of all the urls to further blog posts on the
    page.
    """
    response = requests.get("https://codeup.com/blog/", headers={"user-agent": "Codeup Data Science"})
    soup = BeautifulSoup(response.text)
    links = [link.attrs["href"] for link in soup.select(".more-link")]
    return links

def parse_codeup_blog_article(url):
    "Given a blog article url, extract the relevant information and return it as a dictionary."
    response = requests.get(url, headers={"user-agent": "Codeup Data Science"})
    soup = BeautifulSoup(response.text)
    return {
        "title": soup.select_one(".entry-title").text,
        "published": soup.select_one(".published").text,
        "content": soup.select_one(".entry-content").text.strip(),
    }

def get_blog_articles():
    "Returns a dataframe where each row is a blog post from the codeup blog landing page."
    links = get_front_page_links()
    df = pd.DataFrame([parse_codeup_blog_article(link) for link in links])
    return df


# Acquire InShorts Articles

def parse_news_card(card, category):
    '''
    Take in a news card and generate a dictionary
    '''
    cards = soup.select_one('div.news-card')
    output = {}
    output['category'] = category
    output['title'] = card.select_one('a.clickable').text.strip()
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
    return df