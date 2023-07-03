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
from multiprocessing import Process
from threading import Thread
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_refer_url(article_urls, id_list, start, end, step):
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)                                      # 隐式等待10秒

    refer_url = []
    for url_id in range(start, end, step):
        if id_list:
            url_id = id_list[url_id]
        url = article_urls[url_id-1]    # 编码序号与读取序号相差1
        print(url)
        # url = 'https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=%20CJFD&dbname=CJFDAUTO&filename=HXGC202209016'
        print(f'第{url_id}个url开始获取')
        try:
            driver.get(url)                             # 文章详情页
            time.sleep(random.uniform(4, 6))  # 等待页面加载
        except Exception as e:
            print(f"网页打开失败：{e}")
            driver.close()
            time.sleep(30)
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(10)
            driver.get(url)  # 知网首页地址
            time.sleep(random.uniform(4, 6))  # 等待页面加载
        try:
            f = open(f'html5/refer_{url_id}.html', 'ab')

            iframe = driver.find_element_by_id('frame1')
            driver.switch_to.frame(iframe)
            html = driver.page_source
            f.write(html.encode("utf-8", "ignore"))
            time.sleep(random.uniform(2, 3))  # 等待页面加载

            if driver.find_elements_by_xpath("//div[@class='pageBar']/span"):
                page_list = driver.find_elements_by_xpath("//div[@class='pageBar']/span")
                attr = []
                for i in range(len(page_list)):
                    attr.append(page_list[i].get_attribute("id"))
                for i in range(len(page_list)):
                    # print(i)
                    a = attr[i]
                    while driver.find_elements_by_xpath(f"//span[@id='{a}']/a[text()='下一页']"):
                        # print(i)
                        print("ok")
                        element = driver.find_element_by_xpath(f"//span[@id='{a}']/a[text()='下一页']")
                        driver.execute_script("arguments[0].click();", element)
                        html = driver.page_source
                        f.write(html.encode("utf-8", "ignore"))
                        time.sleep(random.uniform(2, 3))  # 等待页面加载
        except Exception as e:
            print(f"参考文献出错：{url}:{e}")
            # refer_url.append([url_id,url])
        if url_id % 50 ==0:
            # pf2 = pd.DataFrame(refer_url)
            # pf2.to_csv('new_refer_next_fail_url.csv', index=0, header=0, mode='a')
            # refer_url = []
            driver.close()
            time.sleep(10)
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(10)


def process_refer_html(path, output):
    dir = os.listdir(path)
    refer_list = []
    k = 0
    for file in dir:
        art_id = file.strip('.html').split('_')[1]
        # print(art_id)
        htmls = open(path + '\\' + file, 'r', encoding='utf-8').read()
        htmls = htmls.split('</html>')
        for html in htmls:
            if html:
                html = HTML(html + '</html>')
                essayBox = html.xpath('//div[@class="essayBox"]')
                for i in range(len(essayBox)):
                    # print(len(essayBox))
                    type = html.xpath(f'//div[@class="essayBox"][{i + 1}]//div[@class="dbTitle"]/text()')[0]
                    counts = html.xpath(f'//div[@class="essayBox"][{i + 1}]//span[@name="pcount"]/text()')[0]
                    liBox = html.xpath(f'//div[@class="essayBox"][{i + 1}]//li')
                    for j in range(len(liBox)):
                        msg = html.xpath(
                            f'normalize-space(//div[@class="essayBox"][{i + 1}]//li[{j + 1}])')
                        sub_id = msg.strip().strip('[').split(']',1)[0]
                        detail = msg.strip().strip('[').split(']',1)[1].strip()
                        urls = html.xpath(
                            f'//div[@class="essayBox"][{i + 1}]//li[{j+1}]/a[@target="kcmstarget"]/@href')
                        if urls:
                            url = urls[0].strip()
                        else:
                            url = html.xpath(
                            f'//div[@class="essayBox"][{i + 1}]//li[{j+1}]/a/@onclick')
                            if url:
                                url = url[0].split("'")[1]
                            else:
                                url = ''
                        refer = [art_id, sub_id, detail, url, type, counts]
                        refer_list.append(refer)
            # print(refer_list[-1])
        k = k+1
        if k % 100 == 0:
            print(f"已完成{k}条！")
            pf = pd.DataFrame(refer_list)
            pf.to_csv(f"{output}", index=0, header=0, mode='a')
            refer_list=[]

    print(f"已完成{k}条！")
    pf = pd.DataFrame(refer_list)
    pf.to_csv(f"{output}", index=0, header=0, mode='a')


def precess_refer_url(output, output_left):
    refer_info = []
    refer_left = []
    i = 0
    for refer in refer_urls:
        # print(refer[3])
        if pd.isna(refer[3]):
            refer_info.append(refer)
        elif refer[3].startswith('https'):
            refer_info.append(refer)
        elif refer[3].startswith('/kcms'):
            dbcode = re.findall(r'dbcode=(.*?)&', refer[3])
            dbname = re.findall(r'dbname=(.*?)&', refer[3])
            filename = re.findall(r'filename=(.*?)&', refer[3])
            if dbcode:
                dbcode = dbcode[0]
            else:
                dbcode = ''
            if dbname:
                dbname = dbname[0]
            else:
                dbname = ''
            if filename:
                filename = filename[0]
            else:
                filename = ''
            refer[
                3] = f'https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode={dbcode}&dbname={dbname}&filename={filename}'
            # print(refer)
            refer_info.append(refer)
        else:
            # print(refer[3])
            # refer_info.append(refer)
            refer_left.append(refer)
        i = i + 1
        if i % 100 == 0:
            print(f'已完成{i}条！')
            pf1 = pd.DataFrame(refer_info)
            pf1.to_csv(f"{output}", index=0, header=0, mode='a')
            pf2 = pd.DataFrame(refer_left)
            pf2.to_csv(f"{output_left}", index=0, header=0, mode='a')
            refer_info = []
            refer_left = []
    print(f'已完成{i}条！')
    pf1 = pd.DataFrame(refer_info)
    pf1.to_csv(f"{output}", index=0, header=0, mode='a')
    pf2 = pd.DataFrame(refer_left)
    pf2.to_csv(f"{output_left}", index=0, header=0, mode='a')


def get_foreign_refer_url(foreign_refers, start, end, step, output):
    results = []
    k = 0
    for url_id in range(start, end, step):
        k = url_id+1
        title = foreign_refers[url_id][3].strip()    # 编码序号与读取序号相差1
        title_html = title.replace(" ","%20")
        # print(title)
        search_url = r"https://scholar.cnki.net/home/search?sw=2&sw-input="+title_html
        # search_url = r'https://scholar.cnki.net/home/search?sw=1&sw-input=Multi-armed%20bandits%20with%20episode%20context'
        # print(search_url)
        print(f'第{k}个url开始获取')
        try:
            response = HTML(requests.get(search_url).text)
            error = response.xpath("//div[@class='errorOrNoData']")
            if error:
                url = '无搜索结果'
                msg = ''
                eq = ''
            else:
                url = response.xpath("//div[@class='argicle-title'][1]/a[1]/@href")[0]
                msg = response.xpath(
                    "normalize-space(//div[@class='argicle-title'][1]/a[1])").strip('.')
                eq = str(msg==title)
        except Exception as e:
            print(f"参考文献出错：{search_url}:{e}")
            url = '搜索失败'
            msg = ''
            eq = ''
            time.sleep(10)
        foreign_refers[url_id].append(url)
        foreign_refers[url_id].append(msg)
        foreign_refers[url_id].append(eq)
        results.append(foreign_refers[url_id])
        time.sleep(3)
        if (k) % 200 ==start-599:
            print(f"No{start} 已完成{(k-603)//step+1}条！")
            pf = pd.DataFrame(results)
            pf.to_csv(f"{output}", index=0, header=0, mode='a', encoding='gb18030')
            results = []
            time.sleep(10)
    print(f"No{start} 已完成{(k-603)//step+1}条！")
    pf = pd.DataFrame(results)
    pf.to_csv(f"{output}", index=0, header=0, mode='a', encoding='gb18030')


def research_foreign_url(refer_left,output):
    results = []
    k = 0
    for refer in refer_left:
        if not refer[8]:
            refer[8] = refer[3].lower() == refer[7].lower()
        if refer[6] == '搜索失败':
            title = refer[3].strip()  # 编码序号与读取序号相差1
            title_html = title.replace(" ", "%20")
            search_url = r"https://scholar.cnki.net/home/search?sw=2&sw-input=" + title_html
            try:
                response = HTML(requests.get(search_url).text)
                error = response.xpath("//div[@class='errorOrNoData']")
                if error:
                    url = '无搜索结果'
                    msg = ''
                    eq = ''
                else:
                    url = response.xpath("//div[@class='argicle-title'][1]/a[1]/@href")[0]
                    msg = response.xpath(
                        "normalize-space(//div[@class='argicle-title'][1]/a[1])").strip('.')
                    eq = str(msg.lower() == title.lower())
            except Exception as e:
                print(f"参考文献出错：{search_url}:{e}")
                url = '搜索失败'
                msg = ''
                eq = ''
                time.sleep(10)
            refer[6] = url
            refer[7] = msg
            refer[8] = eq
        results.append(refer)
        k = k + 1
        if k % 300 == 0:
            print(k)
            pf = pd.DataFrame(results)
            pf.to_csv(f"{output}.csv", index=0, header=None, mode='a')
            results = []
    pf = pd.DataFrame(results)
    pf.to_csv(f"{output}.csv", index=0, header=None, mode='a')


def download_detail(load_list, type, start, end, step, output):
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # options.add_argument("window-size="+screenWidth+","+screenHeight);
    # 设置页面加载策略，none表示非阻塞模式。
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
    driver.implicitly_wait(10)  # 隐式等待10秒
    driver.set_page_load_timeout(10)
    driver.set_window_size(1920, 1080)

    if type==0:
        results = []
        for i in range(start+19405, end, step):
            url = load_list[i][3]  # 编码序号与读取序号相差1
            print(f'第{i+1}个url开始获取')
            try:
                driver.get(url)  # 文章详情页
                # time.sleep(random.uniform(4, 6))  # 等待页面加载
            except Exception as e:
                print(f"网页打开失败：{e}")
                driver.close()
                time.sleep(10)
                driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
                driver.implicitly_wait(10)
                driver.set_page_load_timeout(10)
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                results.append(load_list[i])
                continue
                # time.sleep(random.uniform(4, 6))  # 等待页面加载
            try:
                more = driver.find_element_by_xpath('//a[@id="ChDivSummaryMore"]').get_attribute('style')
                # print(more)
                if more!='display: none;':
                    driver.find_element_by_id('ChDivSummaryMore').click()
                    time.sleep(2)
            except Exception as e:
                print(f"参考文献出错1：{url}:{e}")
                # refer_url.append([url_id,url])
            try:
                html = HTML(driver.page_source)
                # 作者
                author_list = html.xpath('//h3[@id="authorpart"]/span')
                author = ''
                if author_list:
                    author = html.xpath(
                            'normalize-space(//h3[@id="authorpart"]/span[1])')
                    for j in range(1, len(author_list)):
                        author = author+'; ' + html.xpath(
                            f'normalize-space(//h3[@id="authorpart"]/span[{j+1}])')
                # 单位
                org_list = html.xpath('//div[@class="wx-tit"]/h3')
                org = ''
                if len(org_list)>=2:
                    org = html.xpath(
                        'normalize-space(//div[@class="wx-tit"]/h3[2]/*[1])')
                    for j in range(1, len(org_list)):
                        org = org + '; ' + html.xpath(
                            f'normalize-space(//div[@class="wx-tit"]/h3[2]/*[{j + 1}])')
                # 摘要
                summary = ''
                sum_list = html.xpath('//span[@id="ChDivSummary"]')
                if sum_list:
                    summary = html.xpath('normalize-space(//span[@id="ChDivSummary"])')
                # 关键词
                keywords = ''
                key_list = html.xpath('//div[@class="row"]/*[@class="keywords"]')
                if key_list:
                    keywords = html.xpath('normalize-space(//div[@class="row"]/*[@class="keywords"])')

                load_list[i].append(author)
                load_list[i].append(org)
                load_list[i].append(summary)
                load_list[i].append(keywords)
                results.append(load_list[i])
                time.sleep(random.uniform(1, 2))  # 等待页面加载
            except Exception as e:
                print(f"参考文献出错2：{url}:{e}")
            if i % 200 == (start+5) :
                print(f'No{start+1}已完成{i+1}条!')
                pf = pd.DataFrame(results)
                pf.to_csv(f"{output}.csv", index=0, header=None, mode='a')
                results = []
                driver.close()
                time.sleep(10)
                driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
                driver.implicitly_wait(10)
                driver.set_page_load_timeout(10)
        print(f'No{start + 1}已完成{i + 1}条!')
        pf = pd.DataFrame(results)
        pf.to_csv(f"{output}.csv", index=0, header=None, mode='a')

    if type==1:
        results = []
        for i in range(start, end, step):
            url = load_list[i][3]  # 编码序号与读取序号相差1
            if url=='无搜索结果':
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                results.append(load_list[i])
                continue
            print(f'第{i+1}个url开始获取')
            try:
                driver.get(url)  # 文章详情页
                # print(url)
                time.sleep(random.uniform(2, 3))  # 等待页面加载
            except Exception as e:
                print(f"{start}_网页打开失败：{e}")
                driver.close()
                time.sleep(10)
                driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
                driver.implicitly_wait(10)
                driver.set_page_load_timeout(10)
                driver.set_window_size(1920, 1080)
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                results.append(load_list[i])
                continue
                # time.sleep(random.uniform(4, 6))  # 等待页面加载

            try:
                html = HTML(driver.page_source)
                # 作者
                author_list = html.xpath('//div[@id="doc-author-text"]')
                author = ''
                if author_list:
                    author = html.xpath('normalize-space(//div[@id="doc-author-text"][1])')
                # 单位
                org_list = html.xpath('//div[@id="doc-affi-text"]')
                org = ''
                if org_list:
                    org = html.xpath('normalize-space(//div[@id="doc-affi-text"])')
                # 摘要
                summary = ''
                sum_list = html.xpath('//div[@id="doc-summary-content-text"]')
                if sum_list:
                    summary = html.xpath('normalize-space(//div[@id="doc-summary-content-text"])')
                # 关键词
                keywords = ''
                key_list = html.xpath('//div[@id="doc-keyword-text"]')
                if key_list:
                    keywords = html.xpath('normalize-space(//div[@id="doc-keyword-text"])')

                load_list[i].append(author)
                load_list[i].append(org)
                load_list[i].append(summary)
                load_list[i].append(keywords)
                # time.sleep(random.uniform(1, 2))  # 等待页面加载
            except Exception as e:
                print(f"参考文献出错0：{url}:{e}")
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')

            try:
                more_li = driver.find_elements_by_xpath('//*[@class="detail_ori-new__2hr_D"]')
                # print(more)
                if more_li:
                    for m in range(len(more_li)):
                        driver.find_elements_by_xpath(f'//*[@class="detail_ori-new__2hr_D"]')[m].click()
                        time.sleep(2)
            except Exception as e:
                print(f"参考文献出错1：{url}:{e}")
                # refer_url.append([url_id,url])

            try:
                html = HTML(driver.page_source)
                # 标题
                title_t = ''
                title_list = html.xpath('//div[@id="transTitle"]')
                if title_list:
                    title_t = html.xpath('normalize-space(//div[@id="transTitle"])')
                # 摘要
                summary_t = ''
                sum_list = html.xpath('//div[@class="detail_doc-summary-content-text__1jCkA"]')
                if sum_list:
                    summary_t = html.xpath(
                        'normalize-space(//div[@class="detail_doc-summary-content-text__1jCkA"])')
                # 关键词
                keywords_t = ''
                key_list = html.xpath('//div[@class="detail_keyword-context__3wMNm"]/div')
                if len(key_list)>=2:
                    keywords_t = html.xpath('normalize-space(//div[@class="detail_keyword-context__3wMNm"]/div[2])')

                load_list[i].append(title_t)
                load_list[i].append(summary_t)
                load_list[i].append(keywords_t)
                results.append(load_list[i])
                # time.sleep(random.uniform(1, 2))  # 等待页面加载
            except Exception as e:
                print(f"参考文献出错2：{url}:{e}")
                load_list[i].append('')
                load_list[i].append('')
                load_list[i].append('')
                results.append(load_list[i])

            if i % 200 == (start) and i!=start:
                print(f'No{start+1}已完成{i+1}条!')
                pf = pd.DataFrame(results)
                pf.to_csv(f"{output}.csv", index=0, header=None, mode='a')
                results = []
                driver.close()
                time.sleep(10)
                driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
                driver.implicitly_wait(10)
                driver.set_page_load_timeout(10)
                driver.set_window_size(1920, 1080)
        print(f'No{start + 1}已完成{i + 1}条!')
        pf = pd.DataFrame(results)
        pf.to_csv(f"{output}.csv", index=0, header=None, mode='a')





# 7、下载
data = pd.read_csv("new_refer_urls_pro.csv",header=0)
data = data.values.tolist()
load_list = []
type = 1
type_list = ['原文','期刊','国际期刊','中外文题录','博士','硕士','中国会议','国际会议']
for item in data:
    if item[4]==type_list[type*2] or item[4]==type_list[type*2+1]:
        load_list.append(item)
# print(len(load_list))
# download_detail(load_list, type, 3, 4, 1, f'new_result_{type}')
threads = []
start_id =0
end_id = len(load_list)
for n in range(4):
    step = 1
    thread = Thread(target=download_detail,args=(load_list, type, start_id+n*step, end_id, step*4, f'new_result_{type}_{n+1}', ))
    threads.append(thread)
for t in range(0, len(threads)):
    threads[t].start()


# # 1、读取原文信息：url
# article_urls = pd.read_csv("new_article_urls.csv",header=0,usecols=[1],names=['url'])
# article_urls = article_urls['url'].values.tolist()
#
# # 2.1、单进程爬取
# get_refer_url(article_urls, 0, 1, 2, 1)

# # 3、错误数据再读取
# files = os.listdir("D:\PychamProject\数据处理任务\html3")
# id_list = []
# for file in files:
#     id_list.append(int(file.split('refer_')[1].split('.html')[0]))

# # 2.2、多进程爬取
# threads = []
# start_id =1
# end_id = len(article_urls)+1
# for n in range(5):
#     step = 1
#     thread = Thread(target=get_refer_url,args=(article_urls, 0, start_id+n*step, end_id, step*5, ))
#     threads.append(thread)
# for t in threads:
#     t.start()


# # 4、参考文献html处理
# path = r"D:\PychamProject\数据处理任务\html2"
# output_file = r"new_refer_urls.csv"
# process_refer_html(path, output_file)


# # 5、参考文献url处理
# refer_urls = pd.read_csv("new_refer_urls.csv",header=0,encoding='gb18030')
# refer_urls = refer_urls.values.tolist()
# url_file = r'new_refer_urls_pro.csv'
# url_left_file = r'new_refer_urls_left.csv'
# precess_refer_url(url_file, url_left_file)

# # 6、下载参考文献：中外文题录的url
# refer_left = pd.read_csv("new_refer_urls_left.csv",header=None, encoding='gb18030')
# refer_left = refer_left.values.tolist()
# get_foreign_refer_url(refer_left, 0, 1, 1, r'new_refer_urls_pro0.csv')
# # threads = []
# # start_id =0
# # end_id = len(refer_left)
# # for n in range(5):
# #     step = 5
# #     thread = Thread(target=get_foreign_refer_url,
# #                     args=(refer_left, start_id+n*step, end_id, step*5,f'new_refer_urls_left{n}.csv' ))
# #     threads.append(thread)
# # for t in threads:
# #     t.start()

# # 6.2、处理第一次下载失败的中外文题录url
# refer_left = pd.read_csv("new_refer_urls_pro1.csv",header=0)
# refer_left = refer_left.values.tolist()
# research_foreign_url(refer_left,r'new_refer_urls_pro2')










