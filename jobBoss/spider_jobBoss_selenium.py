from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import random
import requests
import parsel


f = open('E:\下载\课0 结课论文\数据可视化\\boss.csv', mode='a', encoding='utf-8-sig', newline='')
csvWriter = csv.DictWriter(f, fieldnames=[
    '标题',
    '地区',
    '薪资',
    '经验时间',
    '学历要求',
    '公司名',
    '公司领域',
    '福利',
    '公司状态',
    '公司规模',
    '详情页',
    '技能要素',
    '所需技能',
])
csvWriter.writeheader() #  写入头


# lis = driver.find_elements_by_css_selector('.job-list ul li')

def get_job_details():
    # lis0 = driver.find_elements(By.CSS_SELECTOR, '.job-list ul li')
    time.sleep(3)
    # for li in lis0:
    #     mouse = li.find_element(By.CSS_SELECTOR, '.job-name a') # 标题
    #     ActionChains(driver).move_to_element(mouse).perform()
    #     time.sleep(3)
    #     break

    lis = driver.find_elements(By.CSS_SELECTOR, '.job-list ul li')
    for li in lis:
        # mouse = li.find_element(By.CSS_SELECTOR, '.job-title')  # 标题
        # ActionChains(driver).move_to_element(mouse).perform()
        # time.sleep(3)
        title = li.find_element(By.CSS_SELECTOR, '.job-name a').text # 标题
        area = li.find_element(By.CSS_SELECTOR, '.job-area').text # 地区
        salary = li.find_element(By.CSS_SELECTOR, '.job-limit .red').text # 薪资
        experience = li.find_element(By.CSS_SELECTOR, '.job-limit p').get_attribute('innerHTML') # 工作经验
        experience_list = experience.split('<em class="vline"></em>')
        experienceTime = experience_list[0]
        experienceSchool = experience_list[1]
        companyName = li.find_element(By.CSS_SELECTOR, '.company-text h3 a').text # 公司名
        companyStyle = li.find_element(By.CSS_SELECTOR, '.company-text p a').text # 公司领域
        welfare = li.find_element(By.CSS_SELECTOR, '.info-desc').text # 公司福利
        companyInclude = li.find_element(By.CSS_SELECTOR, '.company-text p').get_attribute('innerHTML')  # 公司规模
        company_list = companyInclude.split('<em class="vline"></em>')

        # company_list = companyInclude.find_elements_by_class_name('vline')
        if len(company_list) == 2:
            companyPeople = company_list[1]
            companyState = ''
        else:
            companyState = company_list[1]
            companyPeople = company_list[2]

        # 技能需求tag
        skill_list = li.find_element_by_class_name("tags").find_elements_by_class_name("tag-item")
        skillsTool = ''
        for skill_i in skill_list:
            skill_i_text = skill_i.text
            if len(skill_i_text) == 0:
                continue
            skillsTool = skillsTool+skill_i_text+','

        # 鼠标移动后加载的技能需求
        # try:
        #     skillsNeed = li.find_element(By.CSS_SELECTOR, '.detail-bottom-text').text
        # except:
        #     skillsNeed = ''

        detailPage = li.find_element(By.CSS_SELECTOR, '.job-name a').get_attribute('href') # 详情页
        # if detailPage: # 判定是否有详情页
        #     js = 'window.open()'
        #     driver.execute_script(js) # 打开一个新窗口
        #     driver.switch_to.window(window_name=driver.window_handles[-1]) # 切换到最后一个窗口
        #     driver.maximize_window() # 最大化创库
        #     driver.get(detailPage) # 请求详情页
        #     driver.implicitly_wait(10) # 隐式等待
        #     skillsNeed = driver.find_element(By.CSS_SELECTOR, '.text').text
        #     driver.close() # 关闭当前窗口

        time.sleep(random.uniform(0, 2)) # 随机休眠
        # driver.switch_to.window(driver.window_handles[0]) # 切回第一个窗口

        print(title, area, salary, experienceTime, experienceSchool, companyName, companyStyle, welfare,companyState, companyPeople, detailPage, skillsTool, sep=' | ')
        dit = {
            '标题': title,
            '地区': area,
            '薪资': salary,
            '经验时间': experienceTime,
            '学历要求': experienceSchool,
            '公司名': companyName,
            '公司领域': companyStyle,
            '福利': welfare,
            '公司状态': companyState,
            '公司规模': companyPeople,
            '详情页': detailPage,
            '技能要素': skillsTool,
        }
        csvWriter.writerow(dit) # 逐行写入

# def get_skills_desc(desc_url):
#     # 获取详情页所需技能的函数
#     # 加载另一个窗口
#     js = 'window.open()'
#     driver.execute_script(js) # 打开新窗口
#     driver.switch_to.window(window_name=driver.window_handles[-1]) # 切换到刚打开的窗口
#     # 开始加载url
#     driver.get(url=desc_url) # 加载详情页url
#     driver.implicitly_wait(10) # 等待网页加载完成
#     skills_need = driver.find_element(By.CSS_SELECTOR, '.text') # 直接查找描述字段
#     return skills_need

# city_name = ["北京", "上海", "广州", "深圳", "杭州", "天津", "西安", "苏州", "武汉", "厦门", "长沙", "成都", "郑州", "重庆", "南京"]
# city_num = ["101010100", "101020100", "101280100", "101280600", "101210100", "101030100", "101110100",
#             "101190400", "101200100", "101230200",
#             "101250100", "101270100", "101180100", "101040100", "101190100"]

city_name = ["南京"]
city_num = ["101190100"]

for a in range(15):
    url = "https://www.zhipin.com/c" + city_num[a] + "-p100509/?ka=sel-city-" + city_num[a]
    # url = 'https://www.zhipin.com/c100010000/?query=python&ka=sel-city-100010000'
    driver = webdriver.Chrome()
    driver.get(url=url)
    driver.implicitly_wait(10)
    driver.maximize_window() # 最大化窗口
    for page in range(1, 10 + 1):
        print(f'------------------------正在爬取第{page}页内容----------------------------')
        time.sleep(random.uniform(2,5))
        get_job_details() # 获取信息
        next_button = driver.find_element(By.CSS_SELECTOR, '.page .next')
        if 'disabled' in next_button.get_attribute('class'):  # 如果找到，就表示有下一页
            print(f'已经没有了！ 第{page}已经是最后一页！')
            break
        else:
            next_button.click()  # 点击下一页

    driver.quit() # 退出浏览器