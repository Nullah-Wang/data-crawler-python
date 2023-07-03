import random
import re

import pymysql
import requests
from bs4 import BeautifulSoup
import openpyxl
import xlwt
import time

cookie = '__g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1643370243; lastCity=100010000; gdxidpyhxdE=Gmy9iG7l9M%2F6QC3QuugVPKQa2%2BHaLExbdsUb1hrV6EfMAXYtPWbh3%2FDW6lS%2FDBxb2zkk7rs91YHC0QpaLwiVH1BuT0HMZjRfxgd3H%2BtoaMC%2FA87pLtNfSIQ63pEPqgvR%5CWNKp9bQdv%2F7RnBoTOCoKobalvBpe9KAE%5C4hdSjKoeM7m3hE%3A1643371363229; _9755xjdesxxd_=32; YD00951578218230%3AWM_NI=r0XoRi6VdnQy4YfK3jz4EielkH1YyHqOIy3KTKjAg%2FaHkEpx3K0JznKRXtUVQ8Wc6ChZgnocL8krhOX2omMbqcA%2Bl3l2oeAdveJqYkbMEDcUqOS5C2QYyIqqOKVcFIIXYUg%3D; YD00951578218230%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed7cb44f490baa6d144f4928eb2c54b878f8abbae3e8bef9f8cc533a989ffafb52af0fea7c3b92ab2f09890d163f68aac8fd473f887aaacb262baec8b8ae868a998ffbafc44b391879ab2419895a6a2e625a398a5a6f374f19500abf966898e9895d85e93e89984b549ac86a98fee6990e8a593eb459ceea18ed06ab3bd8fccef39b0eea186c470b6bb8692dc61a2938ba5e25fb3919dd6c23a9387b7aaf47b8d959a84c5438b8897b6e637e2a3; YD00951578218230%3AWM_TID=jsVXBEyWzqNFQEFAURZv6dkVgQ8gChJv; wd_guid=6373e43b-b637-4d33-8d50-d96e465a6a71; historyState=state; _bl_uid=k2kwdykUyOkc9Ic9vx7Rbsn8mtay; __l=l=%2Fwww.zhipin.com%2Fc101280100-p100509%2F%3Fpage%3D1%26ka%3Dpage-1&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DTkaMsY-SNe94q7MS9ehyrSoxpmneVqgjlV-zwovJ_Sbtw0nEmBdfpGheaVtn9Wzh%26wd%3D%26eqid%3Dbc72899b0001228d0000000561f3d6f9&g=&s=3&friend_source=0&s=3&friend_source=0; acw_tc=0a099d7216434581409898138e01a5068531a516426b4f97f7bb767e71701f; __c=1643370243; __a=45128452.1643370243..1643370243.146.1.146.146; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1643458955; __zp_stoken__=4ae5dfBgNaD82OkZhQV1ZDS01OWwpTEA%2FVWxlZ3YtD1MtTC9wJEFGQUVcSHA9MhwHHmQHbzMYOiA7KBM3IQ0SPxUQTWo%2FcRcPHCE9eBllfRdqAxJOBW8xBCc5Uw0UBCAdXF01G2BsT1hybB0%3D'




a = 4
data_w = xlwt.Workbook(encoding='utf-8')
table_w = data_w.add_sheet('Sheet1')

base_url = "https://www.zhipin.com"

# job_type = ["Java", "PHP", "web前端", "iOS", "Android", "算法工程师", "数据分析师", "数据架构师", "数据挖掘", "人工智能", " 机器学习", "深度学习"]
job_type = ["数据分析师", "数据挖掘"]
city_name = ["北京", "上海", "广州", "深圳", "杭州", "天津", "西安", "苏州", "武汉", "厦门", "长沙", "成都", "郑州", "重庆", "南京"]
city_num = ["c101010100", "c101020100", "c101280100", "c101280600", "c101210100", "c101030100", "c101110100",
            "c101190400", "c101200100", "c101230200",
            "c101250100", "c101270100", "c101180100", "c101040100", "c101190100"]


def get_user_agent():
    user_list = [
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
        "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
        "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
        "Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00",
        "Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00",
        "Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0",
        "Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62",
        "Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52",
        "Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51",
        "Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50",
        "Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50",
        "Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (X11; Linux i686; U; es-ES) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11",
        "Opera/9.80 (X11; Linux x86_64; U; bg) Presto/2.8.131 Version/11.10",
        "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10",
        "Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10",
        "Opera/9.80 (Windows NT 6.1; Opera Tablet/15165; U; en) Presto/2.8.149 Version/11.1",
        "Opera/9.80 (X11; Linux x86_64; U; Ubuntu/10.10 (maverick); pl) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (X11; Linux i686; U; ja) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (X11; Linux i686; U; fr) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; en-US) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; cs) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 5.1; U;) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01",
        "Mozilla/5.0 (Windows NT 6.1; U; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01",
        "Mozilla/5.0 (Windows NT 6.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; de) Opera 11.01",
        "Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (X11; Linux i686; U; it) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.6.37 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; ko) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1 x64; U; en) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.7.39 Version/11.00"
    ]
    user_agent = random.choice(user_list)
    return user_agent


def get_page(url):
    headers = {
        'user-agent': "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'cookie': cookie,
        'cache-control': "no-cache",
        'referer': 'https://www.zhipin.com/?ka=header-home'

    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text


    except requests.ConnectionError as e:
        print('Error', e.args)


def translate(str):
    line = str.strip()  # 处理前进行相关的处理，包括转换成Unicode等
    pattern = re.compile('[^\u4e00-\u9fa50-9]')  # 中文的编码范围是：\u4e00到\u9fa5
    zh = " ".join(pattern.split(line)).strip()
    outStr = zh  # 经过相关处理后得到中文的文本
    return outStr


def get_job(flag, url, city_name_x):
    time.sleep(2)
    print("1")
    html = get_page(url)
    soup = BeautifulSoup(html, 'lxml')
    job_all = soup.find_all('div', class_="job-primary")
    job_detail = []
    job_detail_list = []
    if (job_all == []):
        print("cookie已过期")
        flag = 0
    for job in job_all:
        try:
            # 职位名
            job_title = job.find('span', class_="job-name").string
            # 薪资
            job_salary = job.find('span', class_="red").string
            # 职位标签
            job_tag1 = job.p.text
            # 公司
            job_company = job.find('div', class_="company-text").a.text
            # 招聘详情页链接
            job_url = base_url + job.find('div', class_="company-text").a.attrs['href']
            # 公司标签
            job_tag2 = job.find('div', class_="company-text").p.text
            # 发布时间
            job_time = job.find('span', class_="job-pub-time").text

            job_acquire = translate(str(job.find('p')))
            job_detail = [job_title, job_salary, job_tag1, job_company, job_url, job_tag2, job_time, job_acquire, city_name_x]
            # print(job_detail)
            job_detail_list.append(job_detail)
        except Exception as e:
            print(str(e))
    return flag, job_detail_list


city_no = 5  # 城市编号
page = str(10)
# key = job_type[1]
# url = base_url + "/" + city_num[2] + "-p100509" + "&page=" + page + "&ka=page-" + page
# print(url)

job_detail_list= []
num = 0
# for j in range(len(city_num)-1):
flag = 1
for i in range(10):
    page = str(i+1)
    url = "https://www.zhipin.com/c" + city_num[a] + "-p100509/?ka=sel-city-" + city_num[a]
    # print(url)
    flag, job_detail_list1 = get_job(flag=flag, url=url, city_name_x=city_name[a])
    if flag==0:
        print(city_name[a]+"完成，共获得"+str(len(job_detail_list)-num)+"条数据")
        print(i)
        break
    else:
        job_detail_list = job_detail_list + job_detail_list1


for j in range(len(job_detail_list)):
    for k in range(9):
        table_w.write(j, k, job_detail_list[j][k])

data_w.save('E:/下载/课0 结课论文/数据可视化/Boss直聘数据%d.xls' % a)