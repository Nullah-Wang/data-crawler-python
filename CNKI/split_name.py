import re
import pandas as pd
import docx

# 请修改第103-106行的文件名等信息

# 读取文件的函数，输入为文件名和文件格式，输出为列表数据，文件中每行/每格文本为一个元素
def read_file(file,format):
    data = []
    if format == 'txt':                             # 读取txt文件
        f = open(file,encoding='utf-8')
        for line in f:
            data.append(line.strip())
        f.close()
    if format == 'csv':                             # 读取csv文件并转换为列表形式
        df = pd.read_csv(file)
        df_li = df.values.tolist()
        for li in df_li:
            if not pd.isna(li):
                data.append(li)
    if format=='xlsx' or format=='xls':             # 读取excel文件并转换为列表形式
        df = pd.read_excel(file)
        df_li = df.values.tolist()
        for li in df_li:
            if not pd.isna(li):
                data.append(li)
    if format=='docx':                              # 读取word文件
        paragraphs = docx.Document(file).paragraphs
        for para in paragraphs:
            data.append(para.text.strip())
    return data


# 拆分姓名的函数，输入为数据列表和分隔符类型，输出为姓名列表，每个姓名为一个元素
def split_name(data,sep):
    if sep=='逗号':                           # 定义逗号分割模板，默认文件中只有姓名
        split_format = ',|，'
    elif sep=='分号':                         # 定义分号分割模板，后续默认文件中有以逗号或冒号或空格分隔的机构名
        split_format = ';|；'
    elif sep=='混合':                         # 定义混合分割模板，后续默认文件中有以逗号或冒号或空格分隔的机构名
        split_format = '\\||;|；'

    results = []
    distracters = []
    current_num = 1
    data_len = len(data)
    for line in data:
        try:
            print("已处理：{}/{}".format(current_num,data_len), end="\r")       # 现实实时进度，由于处理速度很快，几乎不需要
            current_num = current_num + 1
            if sep=='分号' or sep=='混合':
                result=[]
                distracter = []
                if all(x not in line for x in [',','；',';','，','|',]):         # 若该行不存在其他分隔符号
                    names = re.split(r'[ ]+',line)                              # 则默认分隔符为空格
                else:
                    names = re.split(split_format, line)                        # 否则利用分号分隔符或混合分隔符进行分割
                for name in names:                                              # 如果分隔符为分号或混合，删除姓名后以逗号和冒号分割的单位名称
                    name = re.sub('\(.*?\)|（.*?）|《.*?》', '', name)             # 去掉元素中括号和书名号内的内容
                    spl_results = re.split(',|，|：|:',name)                     # 删除姓名后以逗号和冒号分割的单位名称或其他附加信息
                    if len(spl_results)>1:
                        name = spl_results[0].strip()                           # 第一个元素为姓名
                        for i in range(1,len(spl_results)):                     # 第二个以后的为附加信息，加入干扰列表
                            distracter.append(spl_results[i].strip())
                    else:
                        name = spl_results[0].strip()
                    if all(org not in name for org in organization_list) and name !='':     # 判断元素中是否存在机构关键词或是否为空字符串
                        if ' ' in name:                                     # 若单元中存在空格，则判断是否为中文名
                            if ('\u4e00'<= name[0] <= '\u9fff'):            # 若为中文，则利用空格继续分割
                                name_list = re.split(r'[ ]+',name)
                                for name_li in name_list:                   # 对于分割结果，判断是否为中文名或英文译名
                                    if len(name_li)<=4 or '·' in name_li:
                                        result.append(name_li)              # 是，则加入结果列表
                                    elif name !='':
                                        distracter.append(name_li)          # 不是，则加入干扰列表
                            else:
                                result.append(name)                         # 若为英文，则不继续分割
                                                                            # 注意，此处不能排除以分号或|分割的英文机构名，需要人工排查
                        elif len(name) <= 4 or '·' in name:                 # 若单元中不存在空格，则判断结果是否为中文名或英文译名
                                result.append(name)
                        elif name !='':
                            distracter.append(name)
                    elif name !='':                                         # 若元素中存在机构关键词，则加入到干扰列表
                        distracter.append(name)

            else:
                result = []
                names = re.split(split_format,txt)
                for name in names:
                    result.append(name.strip())
            results = results + result
            distracters = distracters + distracter
        except Exception as e:
            print('{}处发生错误：{}'.format(line, e))
    results = list(set(results))        # 删除重复元素
    # print(results)                      # 输出拆分姓名后的结果
    distracters = list(set(distracters))            # 删除重复元素
    distracters.remove('')
    # print(distracters)                        # 输出排除的非姓名文本
    return results, distracters


file = 'authors_zh.txt'         # **自定义**，读入文件名
file_write = 'result.txt'       # **自定义**，写入正确结果的文件名
file_distracters = 'distracters.txt'   # **自定义**，写入干扰文本的文件名
sep = '混合'                     # **自定义**，分隔符类型：分号；逗号；混合（混合暂时只包括"|"和"分号"和" "的混合，不包括"逗号"和"冒号"）
format = file.split('.')[-1]    # 文件格式
organization_list = ['大学','学院','中心','公司','工作部','研究','实验','课题',
                     '管理处','管理局','管理局','电视台','技术厅','评论员','编辑部',
                     'University','School','College']

# 读取文件
data = read_file(file, format)                  # 读取文件并返回数据列表，文件中一行/一格为一个元素
if data:                                        # 判断文件数据是否为空
    results,distracters = split_name(data,sep)              # 执行split_name函数以拆分姓名
    str = '\n'
    with open(file_write, "w",encoding='utf-8') as f:
        f.write(str.join(results))              # 将结果写入txt文档，每个元素一行
    with open(file_distracters, "w",encoding='utf-8') as f:
        f.write(str.join(distracters))              # 将结果写入txt文档，每个元素一行
else:
    print('文件中无数据')

