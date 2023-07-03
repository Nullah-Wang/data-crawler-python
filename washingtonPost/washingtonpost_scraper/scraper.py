import json
import time
import re
import requests
from .parser import parse_page


url_base = 'https://sitesearchapp.washingtonpost.com/sitesearch-api/v2/search.json?count=20&datefilter=displaydatetime:%5BNOW%2fDAY-1YEAR+TO+NOW%2FDAY%2B1DAY%5D&facets.fields=%7B!ex%3Dinclude%7Dcontenttype,%7B!ex%3Dinclude%7Dname&filter=%7B!tag%3Dinclude%7Dcontenttype:(%22Article%22)&highlight.fields=headline,body&highlight.on=true&highlight.snippets=1&query={}&sort=displaydatetime+desc&spellcheck=true&startat={}&callback=angular.callbacks._b'


def has_date(url):
    datepattern = re.compile('\d{4}-\d{2}-\d{2}')
    date_strf = '-'.join(url.strip("/").split('/')[-4:-1])
    if datepattern.match(date_strf):
        return True
    return False

def get_urls_from_a_search_page(query, startat):
    url = url_base.format(query, startat)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    try:
        r = requests.get(url, headers=headers)
        # len('/**/angular.callbacks._b(') = 25
        response = json.loads(r.text[25:-2])

        urls = [doc.get('contenturl', None) for doc in response.get('results', {}).get('documents', {})]
        print("================")
        print(urls)
        urls = [url for url in urls if url is not None and '//www.washingtonpost.com/' in url]
        urls_date = [url for url in urls if has_date(url)]
        urls_no_date = [url for url in urls if not has_date(url)]
        print(urls_no_date)
        print("================")
        return urls_date, urls_no_date
    except Exception as e:
        print(e)
        return []

def yield_articles_from_search_result(query, max_num=100, sleep=1.0):
    max_num_ = 20 if max_num < 20 else max_num
    n_num = 0
    for startat in range(0, max_num_, 20):
        print('start at = {}'.format(startat))
        try:
            urls = get_urls_from_a_search_page(query, startat)
            if not urls:
                break
        except:
            print('Getting response exception. sleep 15 minutes ...')
            time.sleep(600)
        # terminate
        if not urls or n_num >= max_num:
            return None
        for url in urls:
            time.sleep(sleep)
            if n_num >= max_num:
                break
            try:
                yield parse_page(url)
                n_num += 1
            except Exception as e:
                print(e)
                print('Parsing exception. sleep 5 minutes ...')
                time.sleep(300)
                continue