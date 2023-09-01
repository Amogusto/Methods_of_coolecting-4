import sys
import requests
from lxml import html
from pprint import pprint
from datetime import datetime, date
from pymongo import MongoClient

_LINK_LENTARU = 'https://lenta.ru/'

_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.4.837 Yowser/2.5 Safari/537.36'}

def _parse_news_lentaru():

    req = requests.get(_LINK_LENTARU, headers=_HEADERS)

    dom = html.fromstring(req.text)

    news_list = list()
    news = dom.xpath("//div[@class='topnews']/div/a")

    for item in news:
        element = {}

        news_name = item.xpath('.//div/h3/text()')
        news_link = item.xpath('.//@href')
        news_date = item.xpath('.//div/div/time/text()')

        element['date'] = news_date
        element['name'] = news_name
        element['link'] = news_link
        element['source'] = 'lenta.ru'

        news_list.append(element)


    return news_list

def _parse_news():

    news_list = list()
    news_list.extend(_parse_news_lentaru())
    pprint(news_list)

    return news_list


def _main():

    news_list = _parse_news()

    client = MongoClient()
    db = client['news']
    news = db.news

    for item in news_list:
        news.update_one(item, {'$setOnInsert': item}, upsert=True)


if __name__ == '__main__':
    sys.exit(_main())

_parse_news()

