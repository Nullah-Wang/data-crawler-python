import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import re
import pandas as pd
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import random
import requests
from lxml.etree import HTML
from urllib.parse import urlparse, parse_qs
import os



def get_article_detail(urls, file_success,file_fail):
    # filename = parse_qs(urlparse(url).query)['filename'][0]
    # filepath = f'{self.paper_html_dir}/{filename}.html'
    success = []
    fail = []
    i = 1
    print(urls)
    for url in urls:
        try:
            response = HTML(requests.get(url).text)
            article = response.xpath('//div[@class="doc-top"]')[0]
            article_info = {}
            article_info['title'] = article.xpath('//div[@class="wx-tit"]/h1/text()')[0]
            params = parse_qs(urlparse(url).query)
            dbcode = params['DbCode'][0]
            dbname = params['dbname'][0]
            filename = params['filename'][0]
            article_info['filename'] = filename
            article_info['article_url'] = f'https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode={dbcode}&dbname={dbname}&filename={filename}'
        except:
            print(f'url获取失败：{url}')
            time.sleep(10)
            # article_info['authors'] = ''
            # article_info['organization'] = ''
            # article_info['summary'] = ''
            # article_info['keywords'] = ''
            # article_info['journal'] = ''
            # article_info['publish_time'] = ''
            # success.append(article_info)
        try:
            article_info['authors'] = '; '.join(article.xpath('///h3[@id="authorpart"]/span/a/text()'))
            article_info['organization'] = article.xpath('string(//div[@class="wx-tit"]/h3[2])')
            article_info['summary'] = article.xpath('//span[@id="ChDivSummary"]/text()')[0]
            article_info['keywords'] = article.xpath('normalize-space(//p[@class="keywords"])')
            article_info['journal'] = article.xpath('//div[@class="top-tip"]/span/a/text()')
            article_info['publish_time'] = article.xpath('//div[@class="head-time"]/span/text()')
            print(article_info)
            success.append(article_info)
        except:
            print(f'详情获取失败：{url}')
            fail.append(url)
        i = i+1

    pf1 = pd.DataFrame(success)
    pf2 = pd.DataFrame(fail)
    pf1.to_csv(file_success, index=0, header=0, mode='a',encoding='utf-8')
    pf2.to_csv(file_fail, index=0, header=0, mode='a',encoding='utf-8')
    return success,fail
        # try:
        #     item['cited_num'] = tr.xpath('td[6]/span[@class="KnowledgeNetcont"]/a/text()')[0]
        # except IndexError:
        #     item['cited_num'] = 0
        # try:
        #     item['download_num'] = tr.xpath('td[7]/span[@class="downloadCount"]/a/text()')[0]
        # except IndexError:
        #     item['download_num'] = 0


        # self.write_html(response.text, filepath)
        # if self.get_file_size(file_path=filepath) < 5:
        #     print(f'{url}\t下载失败')
        #     exit()
        # print(f'{url}\t下载完成')


path = r'D:\PychamProject\数据处理任务\html'
dir = os.listdir(path)
refer_list = []
for file in dir:
    art_id = file.strip('.html').split('_')[1]
    print(art_id)
    htmls = open(path + '\\' + file, 'r', encoding='utf-8').read()
    htmls =htmls.split('</html>')
    htmls.pop()
    for html in htmls:
        html = HTML(html+'</html>')
        essayBox = html.xpath('//div[@class="essayBox"]')
        for i in range(len(essayBox)):
            print(len(essayBox))
            type = html.xpath(f'//div[@class="essayBox"][{i+1}]//div[@class="dbTitle"]/text()')[0]
            print(type)
            urls = html.xpath(f'//div[@class="essayBox"][{i+1}]//a[@target="kcmstarget"]/@href')
            # print(urls)
            # print(len(urls))
            for url in urls:
                refer = [art_id, url.strip(), type]
                refer_list.append(refer)
        print(refer_list[-1])

pf = pd.DataFrame(refer_list)
pf.to_csv("refer_url.csv",index=0,header=0)

# article_urls = pd.read_csv("article_info.csv",header=None,usecols=[2],names=['urls'])
# article_urls = article_urls['urls'].values.tolist()
# download_pdf(article_urls)
