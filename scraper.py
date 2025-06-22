import bs4
import requests
import datetime
import json

def scrape_news(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup

def convert_date(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%b %d, %Y')
    except ValueError:
        date_obj = datetime.datetime.strptime(date_str, '%d %B %Y')
    return date_obj.date()

def get_news(tag, url):
    func_map = {
        'league': get_league_news,
        'mtg': get_mtg_news,
        'osrs': get_osrs_news,
        'wow': get_wow_news,
        'pokemon': get_pokemon_news,
        'brighter_shores': get_brighter_shores_news,
        'poe': get_poe_news
    }
    func = func_map.get(tag)
    if func:
        return func(url)
    return None

def get_league_news(url):
    soup = scrape_news(url)
    news = []
    for article in soup.find_all('div', class_='summary'):
        date = convert_date(article.find('time', class_='summary__date').text.strip())
        print(f"Article date: {date}")
        if date == datetime.datetime.now().date():
            title = article.find('span', class_='is-vhidden').text
            description = article.find('div', class_='summary__sell copy copy--muted').text
            link = article.find('a')['href']
            news.append(link)
    print(f"League of Legends news found: {len(news)} current articles")
    return news

def get_mtg_news(url):
    print(f"Scraping Magic: The Gathering news from {url}")
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('article')
    i = 0
    print(f"Found {len(articles)} articles on the page.")
    while i < len(articles):
        link_suffix = articles[i].find('a', attrs={"data-navigation-type": "client-side", "data-link-type": "router"})['href']
        link = f'https://magic.wizards.com{link_suffix}'
        current_article_soup = scrape_news(link)
        date = convert_date(current_article_soup.find('time').text.strip())
        print(f"Article date: {date}")
        if date == datetime.datetime.now().date():
            print(f'Found article with date: {date}, adding to news list.')
            news.append(link)
            i += 1
        else:
            i += 1
    print(f"Magic: The Gathering news found: {len(news)} current articles")
    return news

def get_osrs_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('article')
    print(f"Found {len(articles)} articles on the page.")
    for article in articles:
        date = convert_date(article.find('time').text.strip())
        if date == datetime.datetime.now().date():
            news.append(article.find('a')['href'])
    print(f"Old School RuneScape news found: {len(news)} current articles")
    return news

def get_wow_news(url):
    soup = scrape_news(url)
    news = []
    article_container = soup.find_all('div', class_='List List--vertical List--separatorAll List--full')
    for article_list in article_container:
        articles = article_list.find_all('div', class_='List-item')
        print(f"Found {len(articles)} articles in the list.")
        for article in articles:
            date_div = article.find('div', class_='NewsBlog-date LocalizedDateMount')
            if not date_div:
                continue
            data_props = date_div.get('data-props')
            if not data_props:
                continue
            try:
                iso8601 = json.loads(data_props)['iso8601']
                dt = datetime.datetime.fromisoformat(iso8601.replace('Z', '+00:00'))
                article_date = dt.date()
                print(f"Article date: {article_date}")
                if article_date == datetime.datetime.now().date():
                    link_tag = article.find('a', class_='Link NewsBlog-link')
                    if link_tag and link_tag.has_attr('href'):
                        news.append('https://worldofwarcraft.blizzard.com' + link_tag['href'])
            except Exception as e:
                print(f"Error parsing date from data-props: {data_props} ({e})")
    print(f"World of Warcraft news found: {len(news)} current articles")
    return news

def get_pokemon_news(url):
    soup = scrape_news(url)
    news = []
    print(soup.prettify())
    news_lists = soup.find_all('div', class_='news-list')
    print(f"Found {len(news_lists)} news-list containers on the page.")
    for news_list in news_lists:
        ul = news_list.find('ul')
        if not ul:
            continue
        for li in ul.find_all('li'):
            a_tag = li.find('a', href=True)
            date_p = li.find('p', class_='date')
            if not a_tag or not date_p:
                continue
            date = convert_date(date_p.text.strip())
            if date == datetime.datetime.now().date():
                news.append('https://www.pokemon.com' + a_tag['href'])
    print(f"Pokemon news found: {len(news)} current articles")
    return news

def get_brighter_shores_news(url):
    soup = scrape_news(url)
    news = []
    articles = soup.find_all('div', class_='col-md-4 mb-4')
    print(f"Found {len(articles)} articles on the page.")
    for article in articles:
        try:
            date = article.find('span', class_='editor small text-white').text
        except AttributeError:
            date = article.find('span', class_='editor small').text
        if 'Today' in date:
            news.append(article.find('a')['href'])
    print(f"Brighter Shores news found: {len(news)} current articles")
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
        if date == datetime.datetime.now().date():
            link_set = list(set(article.find_all('a')['href']))
            news.append(link_set[0])
    print(f"Path of Exile news found: {len(news)} current articles")
    return news



