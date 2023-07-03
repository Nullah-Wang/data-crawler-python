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


def get_journal_urls():
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(4)                                      # 隐式等待10秒

    driver.get('https://kns.cnki.net/kns8/AdvSearch?dbprefix=CFLS&&crossDbcodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCJD%2CCCVD%2CCJFN')                             # 知网首页地址
    # driver.find_element_by_id('txt_SearchText').send_keys('芯片')    # 输入关键词
    driver.find_element_by_xpath('//input[@data-tipid="gradetxt-3"]').send_keys('计算机学报')  # 输入关键词
    time.sleep(3)  # 等待页面加载
    # 手动更改时间
    time.sleep(30)  # 等待页面加载
    driver.find_element_by_class_name('btn-search').click()         # 点击检索
    time.sleep(3)  # 等待页面加载
    driver.find_element_by_xpath('//li[@data-id="xsqk"]').click()
    time.sleep(3)  # 等待页面加载
    driver.find_element_by_xpath('//ul[@id="orderList"]/li[2]').click()
    time.sleep(3)  # 等待页面加载
    # driver.find_element_by_xpath('//ul[@id="orderList"]/li[2]').click()
    # time.sleep(3)  # 等待页面加载
    driver.find_element_by_id('perPageDiv').click()
    time.sleep(3)  # 等待页面加载
    driver.find_element_by_xpath('//li[@data-val="50"]').click()
    time.sleep(3)  # 等待页面加载

    # click_page = 9
    # while click_page<31:
    #     driver.find_element_by_id(f'page{click_page}').click()
    #     time.sleep(3)
    #     click_page = click_page+4
    # driver.find_element_by_id('page31').click()
    # time.sleep(3)

    results = []
    j=0
    page = 1
    while page<=20:
        try:
            html = HTML(driver.page_source)
            articles = html.xpath('//div[@id="gridTable"]/table[@class="result-table-list"]/tbody/tr')
            for m in range(1,len(articles)+1):
                url = html.xpath('//tbody/tr[%d]/td[@class="name"]/a/@href' % m)
                title = html.xpath('normalize-space(//tbody/tr[%d]/td[@class="name"])' % m)
                author = html.xpath('normalize-space(//tbody/tr[%d]/td[@class="author"])' % m)
                date = html.xpath('normalize-space(//tbody/tr[%d]/td[@class="date"])' % m)
                journal = html.xpath('normalize-space(//tbody/tr[%d]/td[@class="source"])' % m)
                # author = article.xpath('//td[@class="name"]')[0].text
            # re.findall(r'class="fz14" href="(.*?)"',html)
            # title = re.findall(r'<td class="name">(.*?)</td>',html)
            # author = re.findall(r'<td class="author">(.*?)</td>',html)
            # date = re.findall(r'<td class="date">(.*?)</td>',html)
            # journal = re.findall(r'<td class="data">(.*?)</td>',html)
                result = [page, url[0], title, author, date, journal]
                results.append(result)
            # driver.find_element_by_id('PageNext').click()
            time.sleep(random.uniform(3, 6))  # 等待页面加载
            if page % 5==0:
                pf = pd.DataFrame(results)
                # pf.to_csv("new_article_urls.csv", index=0, header=0, mode='a' ,encoding="utf_8")
                pf.to_csv("new_article_urls3.csv", index=0, header=0, mode='a', encoding="utf_8")
                results = []

                # time.sleep(10)  # 等待页面加载
            if page % 10==0:
                time.sleep(10)
            page = page + 1
        except:
            time.sleep(20)  # 等待页面加载

    driver.close()
    pf = pd.DataFrame(results)
    pf.to_csv("new_article_urls3.csv", index=0, header=0, mode='a' ,encoding="utf_8")
    return results


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
        if i==5:
            break

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


def get_refer_detail(refer_urls, file_success,file_fail):
    # filename = parse_qs(urlparse(url).query)['filename'][0]
    # filepath = f'{self.paper_html_dir}/{filename}.html'
    success = []
    fail = []
    i = 0
    cur_art_id = refer_urls[0][0]
    for url_li in refer_urls:
        if url_li[0] != cur_art_id:
            cur_art_id = url_li[0]
            i = 0
        art_id = url_li[0]
        url = url_li[1]
        type = url_li[2]
        if type=='国际期刊':
            try:
                response = HTML(requests.get(url).text)
                article = response.xpath('//div[@id="__next"]')[0]
                article_info = {}
                article_info['title'] = article.xpath('//div[@id="doc-title"]/text()')[0]
                article_info['article_url'] = url
                article_info['type'] = type
            except Exception as e:
                print(e)
                print(url)
                time.sleep(10)
                article_info['art_id'] = str(art_id)
                article_info['refer_id'] = str(i)
                article_info['authors'] = ''
                article_info['organization'] = ''
                article_info['summary'] = ''
                article_info['keywords'] = ''
                article_info['journal'] = ''
                article_info['publish_time'] = ''
                success.append(article_info)
            try:
                article_info['art_id'] = str(art_id)
                article_info['refer_id'] = str(i)
                article_info['authors'] = ''.join(article.xpath('//div[@id="doc-author-text"]/a/text()'))
                article_info['organization'] = ''
                article_info['summary'] = article.xpath('//div[@id="doc-summary-content-text"]/text()')[0]
                article_info['keywords'] = article.xpath('normalize-space(//div[@id="doc-keyword-text"]/span)')
                article_info['journal'] = article.xpath('string(//div[@id="journal-summarize"])')
                article_info['publish_time'] = article.xpath('//div[@class="head-time"]/span/text()')
                print(article_info)
                success.append(article_info)
            except Exception as e:
                print(e)
                print(url)
                fail.append([art_id, url])
                article_info['art_id'] = str(art_id)
                article_info['refer_id'] = str(i)
                article_info['authors'] = ''
                article_info['organization'] = ''
                article_info['summary'] = ''
                article_info['keywords'] = ''
                article_info['journal'] = ''
                article_info['publish_time'] = ''
                success.append(article_info)
        elif type == '报纸':
            try:
                response = HTML(requests.get(url).text)
                article = response.xpath('//div[@class="doc-top"]')[0]
                article_info = {}
                article_info['article_url'] = url
                article_info['type'] = type
                article_info['title'] = article.xpath('//div[@class="wx-tit"]/h1/text()')[0]
            except Exception as e:
                print(e)
                print(url)
                time.sleep(10)
                article_info['art_id'] = str(art_id)
                article_info['refer_id'] = str(i)
                article_info['authors'] = ''
                article_info['organization'] = ''
                article_info['summary'] = ''
                article_info['keywords'] = ''
                article_info['journal'] = ''
                article_info['publish_time'] = ''
                success.append(article_info)
            try:
                article_info['art_id'] = str(art_id)
                article_info['refer_id'] = str(i)
                article_info['authors'] = '; '.join(article.xpath('///h3[@id="authorpart"]/span/a/text()'))
                article_info['organization'] = article.xpath('string(//div[@class="wx-tit"]/h3[2])')
                article_info['summary'] = article.xpath('//span[@class="abstract-text"]/text()')[0]
                article_info['keywords'] = article.xpath('normalize-space(//p[@class="keywords"])')
                article_info['journal'] = article.xpath('//div[@class="top-tip"]/span/a/text()')
                article_info['publish_time'] = article.xpath('/div[@class="row"]/p/text()')
                print(article_info)
                success.append(article_info)
            except Exception as e:
                print(e)
                print(url)
                fail.append([art_id,url])
                article_info['art_id'] = str(art_id)
                article_info['refer_id'] = str(i)
                article_info['authors'] = ''
                article_info['organization'] = ''
                article_info['summary'] = ''
                article_info['keywords'] = ''
                article_info['journal'] = ''
                article_info['publish_time'] = ''
                success.append(article_info)
        else:
            try:
                url = r'https://kns.cnki.net'+url
                response = HTML(requests.get(url).text)
                article = response.xpath('//div[@class="doc-top"]')[0]
                article_info = {}
                article_info['title'] = article.xpath('//div[@class="wx-tit"]/h1/text()')[0]
                article_info['article_url'] = url
                article_info['type'] = type
            except Exception as e:
                print(e)
                print(url)
                time.sleep(10)
                article_info['art_id'] = str(art_id)
                article_info['refer_id'] = str(i)
                article_info['authors'] = ''
                article_info['organization'] = ''
                article_info['summary'] = ''
                article_info['keywords'] = ''
                article_info['journal'] = ''
                article_info['publish_time'] = ''
                success.append(article_info)
            try:
                article_info['art_id'] = str(art_id)
                article_info['refer_id'] = str(i)
                article_info['authors'] = '; '.join(article.xpath('///h3[@id="authorpart"]/span/a/text()'))
                article_info['organization'] = article.xpath('string(//div[@class="wx-tit"]/h3[2])')
                article_info['summary'] = article.xpath('//span[@id="ChDivSummary"]/text()')[0]
                article_info['keywords'] = article.xpath('normalize-space(//p[@class="keywords"])')
                article_info['journal'] = article.xpath('//div[@class="top-tip"]/span/a/text()')
                article_info['publish_time'] = article.xpath('//div[@class="head-time"]/span/text()')
                print(article_info)
                success.append(article_info)

            except Exception as e:
                print(e)
                print(url)
                fail.append([art_id, url])
                article_info['art_id'] = str(art_id)
                article_info['refer_id'] = str(i)
                article_info['authors'] = ''
                article_info['organization'] = ''
                article_info['summary'] = ''
                article_info['keywords'] = ''
                article_info['journal'] = ''
                article_info['publish_time'] = ''
                success.append(article_info)
        i = i + 1
        if len(success) % 100 ==0:
            time.sleep(10)
        if len(success) % 500 == 0:
            pf1 = pd.DataFrame(success)
            pf2 = pd.DataFrame(fail)
            pf1.to_csv(file_success, index=0, header=0, mode='a',encoding='utf-8')
            pf2.to_csv(file_fail, index=0, header=0, mode='a',encoding='utf-8')
            success = []
            fail = []
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


def download_reference_page(article_info):
    i = 1
    for info in article_info:
        url = info[2]
        query = urlparse(url).query
        filename = info[1]
        print(query)
        refer_urls = f"https://kns.cnki.net/kcms/detail/frame/list.aspx?{query}&RefType=5&vl="
        try:
            headers = {
                'Upgrade-Insecure-Requests': '1',
                'Host': 'kns.cnki.net',
                'Cookie': 'Ecp_ClientId=7191102150100801837; cnkiUserKey=d5f7f03f-22af-3775-8d3b-8a26cab33015; KNS_DisplayModel=listmode@CFLS; RsPerPage=50; KNS_SortType=CFLS%21%28FFD%252c%2527RANK%2527%29+desc; ASP.NET_SessionId=yc2srb0vatkcubu440fwcqaj; SID_kcms=124118; SID_krsnew=125134; _pk_ses=*; LID=WEEvREcwSlJHSldRa1FhdkJkVG5ha1U3OXdrbWpHSE1XcjZYdXYvZ0lZVT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; SID_klogin=125143; c_m_LinID=LinID=WEEvREcwSlJHSldRa1FhdkJkVG5ha1U3OXdrbWpHSE1XcjZYdXYvZ0lZVT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=11/04/2019 15:36:27; c_m_expire=2019-11-04 15:36:27; Ecp_session=1; Ecp_LoginStuts=%7B%22IsAutoLogin%22%3Afalse%2C%22UserName%22%3A%22SH0184%22%2C%22ShowName%22%3A%22%25E5%25AE%2581%25E6%25B3%25A2%25E5%25B7%25A5%25E7%25A8%258B%25E5%25AD%25A6%25E9%2599%25A2%22%2C%22UserType%22%3A%22bk%22%2C%22r%22%3A%22ZU2XWU%22%7D',
                'User-Agent': 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36 Edg/106.0.1370.42',
                'Referer': f'https://kns.cnki.net/KCMS/detail/detail.aspx?{query}',
            }

            onclick = "WriteKrsDownLog()"
            target = "_blank"
            id = "pdfDown"
            name = "pdfDown"
            href = "https://bar.cnki.net/bar/download/order?id=jBGETXBNdPImvx70aLAuJPjDI3A2vZL8vlJ5Yxju1VId5xqCn4BdOA3FtBrcgdmdkLawSrNNEjHzfic%2bAWICsIXNr%2bq%2fxAZGaJQaVfGy3LZXUusYHsGzJp9yrhvnk3r3JRJIuitYASY3ZPhq07jV3E2KrDbH2i1UsOVLzAXdpwmbKKoXvHPzsB%2bN7b8wc5953SA6ol%2becniTwUstlDefatr%2b93LrdvkD9CwUbXbsT4sYgW1T3oFZ4xO0eVG7BcLs"
            response = requests.get(refer_urls, headers=headers)
            if response.status_code == 200:
                info.extend(str(i))
                info.extend('0')
                pf1 = pd.DataFrame(info)
                pf1.to_csv('refer_success.csv', index=0, header=0, mode='a',encoding='utf-8')
                print(response.text)
                # get_article_detail(refer_urls,'refer_success.csv','refer_fail.csv',i)
                i = i+1
                # if i % 5 ==0:
                #     time.sleep(10)
            else:
                print('else')
                raise Exception(f"请求异常, 状态码为：{response.status_code}")
                time.sleep(200)
        except Exception as e:
            print(f'{refer_urls}\t下载失败:{e}')


get_journal_urls()

# urls = pd.read_csv("journal_urls3.csv",header=None,names=['urls'],skiprows=range(3))
# urls = urls['urls'].values.tolist()
# # print(urls)
# get_article_detail(urls,'article_info_test.csv','article_info_fail_test.csv')

# article_info = pd.read_csv("article_info.csv",header=None,nrows=1)
# article_info = article_info.values.tolist()
# # print(article_info)
# download_reference_page(article_info)

# refer_urls = pd.read_csv("refer_url.csv",header=None)
# refer_urls = refer_urls.values.tolist()     # art_id,url,journal_type
# get_refer_detail(refer_urls,'refer_info.csv','refer_info_fail.csv')

