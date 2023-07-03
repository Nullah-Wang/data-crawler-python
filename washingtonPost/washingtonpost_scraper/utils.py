import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import gmtime, strftime
import multiprocessing
from multiprocessing import Pool


news_dateformat = '%B. %d, %Y'
user_dateformat = '%Y-%m-%d'

def now():
    """
    Returns
    -------
    Current time : str
        eg: 2018-11-22 13:35:23
    """
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_soup(url, headers=None):
    """
    Arguments
    ---------
    url : str
        Web page url
    headers : dict
        Headers for requests. If None, use Mozilla/5.0 as default user-agent
    Returns
    -------
    soup : bs4.BeautifulSoup
        Soup format web page
    """

    if headers is None:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    try:
        r = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        return None
    html = r.text
    page = BeautifulSoup(html, 'lxml')
    return page

doublespace_pattern = re.compile('\s+')
lineseparator_pattern = re.compile('\n+')

def normalize_text(text):
    text = text.replace('\t', ' ')
    text = text.replace('\r', ' ')
    text = lineseparator_pattern.sub('\n', text)
    text = doublespace_pattern.sub(' ', text)
    return text.strip()

def strf_to_datetime(strf, form):
    return datetime.strptime(strf, form)

def save(json_obj, date, directory):
    title = json_obj['title'][:50].replace(' ','-')
    path = '{}/{}_{}.json'.format(directory, date, title)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_obj, f, indent=2, ensure_ascii=False)