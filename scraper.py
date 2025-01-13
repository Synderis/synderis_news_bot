import bs4
import requests
import pandas as pd
import datetime

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
    else:
        return None

def get_league_news(url):
    soup = scrape_news(url)
    news = []
    for article in soup.find_all('div', class_='summary'):
        date = convert_date(article.find('time', class_='summary__date').text.strip())
        if date == datetime.datetime.now().strftime('%m/%d/%Y'):
            title = article.find('span', class_='is-vhidden').text
            description = article.find('div', class_='summary__sell copy copy--muted').text
            link = article.find('a')['href']
            news.append(link)
    return news

def get_mtg_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('article')
    i = 0
    while i < len(articles):
        link = articles[i].find('a', attrs={"data-navigation-type": "news", "data-link-type": "router"})['href']
        current_article_soup = scrape_news(link)
        date = convert_date(current_article_soup.find('time').text.strip())
        if date == datetime.datetime.now().strftime('%m/%d/%Y'):
            news.append(link)
            i += 1
        elif date < datetime.datetime.now().strftime('%m/%d/%Y'):
            break
        else:
            i += 1
    return news

def get_osrs_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('article')
    for article in articles:
        date = convert_date(article.find('time').text.strip())
        if date == datetime.datetime.now().strftime('%m/%d/%Y'):
            news.append(article.find('a')['href'])
    return news

def get_wow_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('div', class_='List List--vertical List--separatorAll List--full').find_all('List-item')
    for article in articles:
        date = article.find('time').text
        if 'Today' in date:
            news.append(article.find('a')['href'])
    return news

def get_pokemon_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('div', class_='news-list').find_all('a')
    for article in articles:
        date = convert_date(article.find('p', class_='date').text.strip())
        if date == datetime.datetime.now().strftime('%m/%d/%Y'):
            news.append(article['href'])
    return news

def get_brighter_shores_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('div', class_='col-md-4 mb-4')
    for article in articles:
        date = article.find('time').text
        if 'Today' in date:
            news.append(article.find('a')['href'])
    return news

def get_poe_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('div', class_='newsList').find_all('div', class_=['newsListItem', 'newsListItem alt'])
    for article in articles:
        date_str = article.find('div', class_='date').text
        parts = date_str.split(',', 2)
        date_part = parts[0] + ',' + parts[1]
        date = convert_date(date_part)
        if date == datetime.datetime.now().strftime('%m/%d/%Y'):
            link_set = list(set(article.find_all('a')['href']))
            news.append(link_set[0])
    return news



