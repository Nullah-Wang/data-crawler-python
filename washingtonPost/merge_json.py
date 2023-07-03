import os
import json

# 获取目标文件夹的路径
# filedir = './output/chian&chinese'
# # 获取当前文件夹中的文件名称列表
# filenames = os.listdir(filedir)
# # 打开当前目录下的result.json文件，如果没有则创建
#
# with open('./output/result.json', "w", encoding="utf-8") as f0:  # 结果文件
#     y = 0
#     f0.write('[')
#     f0.write('\n')
#     for filename in filenames:
#         # 文件的个数
#         filepath = filedir + '/' + filename
#         # 该文件中line有多少行
#         # print(filepath + "开始访问...")
#         with open(filepath, 'r', encoding='utf-8')as fp1:
#             y = y + 1
#             print(y)
#             data = json.load(fp1)  # 是列表
#             json.dump(data, f0, ensure_ascii=False,indent=2)
#
#         f0.write("\n,\n")
#     f0.close()


with open('./output/result.json', "r", encoding="utf-8") as f0:
    data = json.load(f0)
    print(data[20000])
f0.close()