import bs4
import requests
import pandas as pd
from datetime import datetime

def scrape_news(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup

def convert_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%b %d, %Y')
    except ValueError:
        date_obj = datetime.strptime(date_str, '%d %B %Y')
    
    return date_obj

def get_news(tag, url):
    if tag == 'league':
        get_league_news(url)
    elif tag == 'mtg':
        get_mtg_news(url)
    elif tag == 'osrs':
        get_osrs_news(url)
    elif tag == 'wow':
        get_wow_news(url)
    elif tag == 'pokemon':
        get_pokemon_news(url)
    elif tag == 'brighter_shores':
        get_brighter_shores_news(url)
    elif tag == 'poe':
        get_poe_news(url)
    else:
        return None

def get_league_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('div', class_='summary')
    i = 0

    while i < len(articles):
        date = convert_date(articles[i].find('time', class_='summary__date').text.strip()).date()
        if date == datetime.now().date():
            link = articles[i].find('a')['href']
            news.append(link)
            i += 1
        else:
            break
    return news

def get_mtg_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find('articles-hub').find_all('a', attrs={"data-navigation-type": "news", "data-link-type": "router"})
    i = 0
    while i < len(articles):
        link = articles[i]['href']
        current_article_soup = scrape_news(link)
        date = convert_date(current_article_soup.find('time').text.strip()).date()
        if date == datetime.now().date():
            news.append(link)
            i += 1
        else:
            break
    return news

def get_osrs_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('news-list-article')
    i = 0
    while i < len(articles):
        date = convert_date(articles[i].find('time').text.strip()).date()
        if date == datetime.now().date():
            news.append(articles[i].find('a')['href'])
            i += 1
        else:
            break
    return news

def get_wow_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('List-item')
    i = 0
    while i < len(articles):
        date = articles[i].find('time').text
        if 'Today' in date:
            news.append(articles[i].find('a')['href'])
            i += 1
        else:
            break
    return news

def get_pokemon_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find('div', class_='news-list').find_all('a')
    i = 0
    while i < len(articles):
        date = convert_date(articles[i].find('p', class_='date').text.strip()).date()
        if date == datetime.now().date():
            news.append(articles[i]['href'])
            i += 1
        else:
            break
    return news

def get_brighter_shores_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('div', class_='col-md-4 mb-4')
    i = 0
    while i < len(articles):
        date = articles[i].find('time').text
        if 'Today' in date:
            news.append(articles[i].find('a')['href'])
            i += 1
        else:
            break
    return news

def get_poe_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('div', class_=['newsListItem', 'newsListItem alt'])
    i = 0
    while i < len(articles):
        date_str = articles[i].find('div', class_='date').text
        parts = date_str.split(',', 2)
        date_part = parts[0] + ',' + parts[1]
        date = convert_date(date_part).date()
        if date == datetime.now().date():
            link_set = list(set(articles[i].find_all('a')['href']))
            news.append(link_set[0])
            i += 1
        else:
            break
    return news



