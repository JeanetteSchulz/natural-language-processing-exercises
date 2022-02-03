############################################# Introduction #############################################

# This  wrangle.py file is for the Codeup NLP Project utilizing Beautiful Soup for web scraping.

# These functions are the work of Jeanette Schulz and are here to create a cleaner work 
# enviroment in jupyter notebook for future presenting. 

############################################### Imports ###############################################

from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd
from time import strftime

########################################### Acquire ###########################################
def front_page_links():
    """
    Short function to hit the codeup blog landing page and return a list of all the urls to further blog posts on the
    page.
    """
    response = get("https://codeup.com/blog/", headers={"user-agent": "Codeup Data Science"})
    soup = BeautifulSoup(response.text)
    links = [link.attrs["href"] for link in soup.select(".more-link")]

    return links

def blog_article(url):
    "Given a blog article url, extract the relevant information and return it as a dictionary."
    response = get(url, headers={"user-agent": "Codeup DS"})
    soup = BeautifulSoup(response.text)
    return {
        # The title of the Article
        "title": soup.select_one(".entry-title").text,
        # The date the article was published
        "published": soup.select_one(".published").text,
        # The actual written blog of the article 
        "content": soup.select_one(".entry-content").text.strip(),
    }

def get_codeup_blogs():
    "Returns a dataframe where each row is a blog post from the front page of the codeup blogs."
    links = front_page_links()
    df = pd.DataFrame([blog_article(link) for link in links])
    return df

def parse_news_card(card):
    'Given a news card object, returns a dictionary of the relevant information.'
    card_title = card.select_one('.news-card-title')
    output = {}
    output['title'] = card.find('span', itemprop = 'headline').text
    output['author'] = card.find('span', class_ = 'author').text
    output['content'] = card.find('div', itemprop = 'articleBody').text
    output['date'] = card.find('span', clas ='date').text
    return output


def parse_inshorts_page(url):
    '''Given a url, returns a dataframe where each row is a news article from the url.
    Infers the category from the last section of the url.'''
    category = url.split('/')[-1]
    response = get(url, headers={'user-agent': 'Codeup DS'})
    soup = BeautifulSoup(response.text)
    cards = soup.select('.news-card')
    df = pd.DataFrame([parse_news_card(card) for card in cards])
    df['category'] = category
    return df

def get_inshorts_articles():
    '''
    Returns a dataframe of news articles from the business, sports, technology, and entertainment sections of
    inshorts.
    '''
    url = 'https://inshorts.com/en/read/'
    categories = ['business', 'sports', 'technology', 'entertainment']
    df = pd.DataFrame()
    for cat in categories:
        df = pd.concat([df, pd.DataFrame(parse_inshorts_page(url + cat))])
    df = df.reset_index(drop=True)
    return df

########################################### Prepare ###########################################
