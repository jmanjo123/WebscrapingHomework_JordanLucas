import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests

browser = Browser('chrome', headless=True)

def newsScraper():
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    source = browser.html
    soup = BeautifulSoup(source, 'html.parser')
    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div', class_='article_teaser_body').text.strip()
    return [news_title, news_p]


def imageScaper():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    source = browser.html
    soup = BeautifulSoup(source, "html.parser")
    containers = soup.find_all('a', class_='fancybox')
    container = containers[1]
    image_url = container['data-fancybox-href']
    image_url = 'https://www.jpl.nasa.gov' + image_url
    return image_url

def tweetScraper():
    url = 'https://twitter.com/marswxreport?lang=en'
    source = requests.get(url)
    soup = BeautifulSoup(source.content, 'html.parser')
    tweet = soup.find('p', class_='tweet-text').text.strip()
    return tweet

def tableScraper():
    tables = pd.read_html('https://space-facts.com/mars/')
    table = tables[0]
    html_table = table.to_html()
    return html_table

def hemisphereScraper():
    results = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    links = browser.find_by_tag('h3')
    i = 0
    for link in links:
        browser.find_by_tag('h3')[i].click()
        source = browser.html
        soup = BeautifulSoup(source, "html.parser")
        title = soup.find('h2').text
        image_url = soup.find('div', class_='downloads').find('a')['href'].strip()
        results.append({"title": title, "img_url": image_url})
        browser.back()
        i = i + 1

    return results

def scrape_all():
    results = {'news_title'   : newsScraper()[0],
               'news_p'       : newsScraper()[1],
               'image_scraped': imageScaper(),
               'tweet_scraped': tweetScraper(),
               'table_scraped': tableScraper(),
               'hemispheres'  : hemisphereScraper()}
    return results