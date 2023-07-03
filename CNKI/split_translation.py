import pandas as pd
import re

# **自定义**，输入excel路径
path_in = r'D:\数据处理代码需求20220929\4.互译文本格式处理\互译文本格式处理.xlsx'
# **自定义**，互译正确文本的输出txt路径
path_out_true = r'D:\数据处理代码需求20220929\4.互译文本格式处理\互译文本格式处理_互译成功数据.txt'
# **自定义**，互译失败中文文本的输出txt路径
path_out_false_ch = r'D:\数据处理代码需求20220929\4.互译文本格式处理\互译文本格式处理_互译失败数据_中文.txt'
# **自定义**，互译失败英文文本的输出txt路径
path_out_false_en = r'D:\数据处理代码需求20220929\4.互译文本格式处理\互译文本格式处理_互译失败数据_英文.txt'


data = pd.read_excel(path_in,usecols=[0,1])
lines = data.values.tolist()
trans_true = []         # 互译成功的列表
trans_false_ch = []     # 互译失败的中文列表
trans_false_en = []     # 互译失败的英文列表
i = 1
lines_len = len(lines)
for line in lines:
    try:
        print("已处理：{}/{}".format(i, lines_len), end="\r")  # 现实实时进度，由于处理速度很快，几乎不需要
        i = i+1
        if isinstance(line[0],str):
            left = line[0].strip().strip('%|;|/')   # 输入预处理
            left_list = re.split('%|;|/',left)      # 输入切片，分隔符为% ; /
        else:
            continue

        if isinstance(line[1],str):
            right = re.sub('\(.*?\)|（.*?）|《.*?》', '', line[1].strip().strip('%|;|/'))    # 输入预处理
            right_list = re.split('%|;|/', right)                                          # 输入切片，分隔符为% ; /
        else:
            right_list = []

        if len(left_list)==len(right_list):                             # 若该行互译文本正确
            trans_true = trans_true + list(zip(left_list,right_list))   # 将该行每对互译文本配对到一个list中
        else:
            for left_item in left_list:                                 # 若该行互译文本有误
                if '\u4e00'<= left_item[0] <= '\u9fff' or '\u4e00'<= left_item[-1] <= '\u9fff':
                    trans_false_ch.append(left_item)                    # 若待翻译文本为中文，输出到中文列表
                else:
                    trans_false_en.append(left_item)                    # 若待翻译文本为英文，输出到英文列表
    except Exception as e:
        print(line)
        print("该行出现错误：{}".format(e))

trans_true = set(trans_true)                    # 结果去重
trans_true = [list(i) for i in trans_true]      # 格式转换，tuple转list
trans_true = sorted(trans_true, key = lambda trans_true_item:trans_true_item[0])      # 结果排序

with open(path_out_true,'w',encoding='utf-8') as f1:
    for trans_true_item in trans_true:
        if '\u4e00'<= trans_true_item[0][0] <= '\u9fff' or '\u4e00'<= trans_true_item[0][-1] <= '\u9fff':
            # print(trans_true_item[0])
            f1.write(trans_true_item[0]+'\t'+trans_true_item[1]+'\n')   # 若翻译成功文本为中文，输出到互译正确列表
        else:
            trans_false_en.append(trans_true_item[0])                   # 若翻译成功文本为英文，输出到英文列表


trans_false_ch = list(set(trans_false_ch))      # 结果去重
trans_false_en = list(set(trans_false_en))      # 结果去重
trans_false_ch.sort()      # 结果排序
trans_false_en.sort()      # 结果排序

# 互译错误的中文列表输出到txt
with open(path_out_false_ch,'w',encoding='utf-8') as f2:
    for trans_false_ch_item in trans_false_ch:
        f2.write(trans_false_ch_item.strip()+'\n')

# 互译错误的英文列表输出到txt
with open(path_out_false_en,'w',encoding='utf-8') as f2:
    for trans_false_en_item in trans_false_en:
        f2.write(trans_false_en_item+'\n')