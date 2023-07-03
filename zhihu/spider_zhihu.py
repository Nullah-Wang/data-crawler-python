import requests
import json
import time
import csv
from lxml import etree
import aiohttp
import asyncio
import hashlib
import execjs
import requests
import random


question_id = "309552331"
question_name = "贴吧为什么还不凉？"


def get_dc0():
    """
    搞一个dc0
    :return:
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36 Edg/98.0.1108.62",
    }
    session = requests.session()
    session.headers = headers
    state1 = 1
    while state1:
        try:
            session.get("https://www.zhihu.com/question/36456390", headers=headers)
            state1=0
        except:
            print(session)
            continue
    dc0 = dict(session.cookies)["d_c0"]
    return dc0


def get_headers(dc0, url):
    """
    执行js加密，获得加密过的请求头
    :param dc0:
    :param url:
    :return:
    """
    x81 = "3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTk7tu6L2qK6P0ET9y-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Ie8FL7AtqM6O1VDQyQ6nxrRPCHukMoCXBEgOsiRP0XL2ZUBXmDDV9qhnyTXFMnXcTF_ntRueTh_29ZrL96Tes_bNMggpmtbSYobSYIuw9_BYBkXOK8gYBCqSm-C20ZueBtGLPvM38TBHKCrXm6HSX8BHm17X1SLH0SrLV6QOKKLH9JQ9Z-JOpxDCmiCLZkJVmegL1LJL1t9YKOh3LbDpV9hcGqUxmOC30wqoKABVZgBVfJ4o9sJx18JN95qfzWUL8pB3xHGSMbgYLeg90X9V8QU2qNUoVcH3qPBCBSLY_18F_OcV_zwpOfrxKwweCUgV1swxmVBCZECV8xcw1DC2xbiVChwC1TvwLkCLBOcHMuwLCe8eC"

    dc0 = '"' + dc0 + '"'
    url = url.replace("https://www.zhihu.com", "")
    code1 = "+".join(["101_3_2.0", url, dc0, x81])
    md5_code = hashlib.md5(bytes(code1, encoding="utf8")).hexdigest()
    ctx2 = execjs.compile(open('zh_96.js', 'r', encoding="utf-8").read(),cwd="C:/Users/Nullah Guri/AppData/Roaming/npm/node_modules")
    encrypt_str = "2.0_" + ctx2.call('b', md5_code)
    headers = {'Host': 'www.zhihu.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
               'x-zse-93': '101_3_2.0', 'sec-ch-ua-mobile': '?0',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36 Edg/98.0.1108.62',
                'x-zst-81': x81,
               'x-requested-with': 'fetch',
               'x-zse-96': encrypt_str,
               'sec-ch-ua': '"NotA;Brand";v="99","Chromium";v="98","GoogleChrome";v="98"',
               'sec-ch-ua-platform': '"Windows"',
               'Accept': '*/*',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Dest': 'empty',
               'Referer https': '//www.zhihu.com/question/36456390',
               'Accept-Encoding': 'gzip,deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
               'Cookie': 'd_c0={};'.format(dc0)}

    return headers


def GetAnswers(question_id):
    i = 0
    while True:
        server_url = "http://127.0.0.1:8080/test"
        print("answer" + str(i))
        url = 'https://www.zhihu.com/api/v4/questions/{0}/answers' \
              '?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%' \
              '2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%' \
              '2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%' \
              '2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%' \
              '2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%' \
              '2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%' \
              '2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&' \
              'limit=5&offset={1}&platform=desktop&sort_by=default'.format(question_id,i)
        print(url)
        state = 1
        while state:
            try:
                dc0 = get_dc0()
                headers = get_headers(dc0, url)
                cookies = {"d_c0": dc0}
                res = requests.get(url, headers=headers,cookies=cookies, timeout=(3, 7))
                state = 0
            except:
                continue
        res.encoding = 'utf-8'
        # print(res.text)
        jsonAnswer = json.loads(res.text)
        # print(jsonAnswer)
        try:
            is_end = jsonAnswer['paging']['is_end']
        except:
            print(jsonAnswer)

        for data in jsonAnswer['data']:
            l = list()
            answer_id = str(data['id'])
            l.append(answer_id)
            l.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['created_time'])))
            l.append(data['author']['name'])
            if(data['content']):
                # print(str(i)+"yes")
                l.append(''.join(etree.HTML(data['content']).xpath('//p//text()')))
            else:
                print(str(i)+"-"+str(i+5)+"之间存在空回答")
                # print(data['content'])
            writer.writerow(l)
            # print(l)

            if data['admin_closed_comment'] == False and data['can_comment']['status'] and data['comment_count'] > 0:
                GetComments(answer_id)

        i += 5
        print('打印到第{0}页'.format(int(i / 5)))

        if is_end:
            break

        time.sleep(random.uniform(1, 2))


def GetComments(answer_id):
    j = 0
    while True:
        url = 'https://www.zhihu.com/api/v4/answers/{0}/root_comments?order=normal&limit=20&offset={1}&status=open'.format(
            answer_id, j)

        print("comments"+str(j))
        state=1
        while state:
            try:
                dc0 = get_dc0()
                headers = get_headers(dc0, url)
                cookies = {"d_c0": dc0}
                res = requests.get(url, headers=headers,cookies=cookies, timeout=(3, 7))
                state=0
            except:
                continue

        res.encoding = 'utf-8'
        jsonComment = json.loads(res.text)
        # print(jsonComment)
        try:
            is_end = jsonComment['paging']['is_end']
        except:
            print(jsonComment)

        for data in jsonComment['data']:
            l = list()
            comment_id = str(answer_id) + "_" + str(data['id'])
            l.append(comment_id)
            l.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['created_time'])))
            l.append(data['author']['member']['name'])
            if (data['content']):
                l.append(''.join(etree.HTML(data['content']).xpath('//p//text()')))
            else:
                print(answer_id + "回答的第" + str(j) + "-" + str(j + 20) + "条评论之间存在空评论")
            writer.writerow(l)
            # print(l)

            for child_comments in data['child_comments']:
                l.clear()
                l.append(str(comment_id) + "_" + str(child_comments['id']))
                l.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(child_comments['created_time'])))
                l.append(child_comments['author']['member']['name'])
                if (child_comments['content']):
                    l.append(''.join(etree.HTML(child_comments['content']).xpath('//p//text()')))
                else:
                    print(answer_id+"回答的第"+str(j) + "-" + str(j + 20) + "条评论之间存在空子评论")
                writer.writerow(l)
                # print(l)
        j += 20
        if is_end:
            break

        time.sleep(1)


csvfile = open('%s_%s.csv' % (question_id,question_name), 'w', newline='', encoding='utf-8-sig')
writer = csv.writer(csvfile)
writer.writerow(['id', 'created_time', 'author', 'content'])

GetAnswers(question_id)
csvfile.close()