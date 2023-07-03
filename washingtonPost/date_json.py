import os
import json
import calendar

# 获取目标文件夹的路径
filedir = './output/china&chinese'
# 获取当前文件夹中的文件名称列表
filenames = os.listdir(filedir)
# 打开当前目录下的result.json文件，如果没有则创建

i = 0
for filename in filenames:
    # 文件的个数
    filepath = filedir + '/' + filename
    # 该文件中line有多少行
    # print(filepath + "开始访问...")
    with open(filepath, 'r', encoding='utf-8')as fp1:
        i = i + 1
        print(i)
        data = json.load(fp1)  # 是列表
        if data["date"]:
            print(data["date"])
            date = data["date"].split(" ")
            print(date)
            y = date[2].split("|")[0]
            m = list(calendar.month_name).index(date[0])
            d = int(date[1].strip(','))
            if m<10:
                if d<10:
                    date_strf = "{}-0{}-0{}".format(y,m,d)
                else:
                    date_strf = "{}-0{}-{}".format(y, m, d)
            else:
                if d<10:
                    date_strf = "{}-{}-0{}".format(y,m,d)
                else:
                    date_strf = "{}-{}-{}".format(y, m, d)
            data["data_strf"] = date_strf
            print(date_strf)
        else:
            print(filename)
            break
    with open(filedir + '/' + date_strf + filename, 'w', encoding='utf-8')as fp2:
        json.dump(data, fp2, ensure_ascii=False,indent=2)

