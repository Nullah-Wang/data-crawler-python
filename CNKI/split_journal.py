import pandas as pd
import re

path_in = r'D:\数据处理代码需求20220929\2.同一行文本拆分\刊名.txt'          # 输入txt路径
path_out = r'D:\数据处理代码需求20220929\2.同一行文本拆分\刊名(处理后).txt'          # 输出txt路径

# 读取txt文件
with open(path_in,'r', encoding='utf-8') as f:
    lines = f.readlines()

# 处理数据
journal_list = []
lines_len = len(lines)
for i in range(lines_len):
    line = lines[i].strip()                         # 去除每行首尾的空格、换行等字复
    journal = re.split(r'[ ]+', line,1)         # 在第一组空格处划分，划分出中文译名和英文译名
    journal_list.append(journal)                # 将结果放入输出list
    print("已处理：{}/{}".format(i+1,lines_len), end="\r")    # 现实实时进度，由于处理速度很快，几乎不需要

# 写入txt文件
with open(path_out,'w', encoding='utf-8') as f:
    for journal in journal_list:
        try:
            if len(journal)>1:                              # 部分结果只有中文译名没有英文译名，进行判定
                f.write(journal[0]+'\t'+journal[1]+'\n')
            else:
                f.write(journal[0]+'\n')
        except Exception as e:
            print('{}处发生错误：{}'.format(journal,e))       # 遇到错误则输出错误位置和错误原因