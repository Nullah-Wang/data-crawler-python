import os
import pandas as pd

art_info = pd.read_csv('article_info.csv',encoding='utf-8')
# print(art_info.loc[0])
# print(art_info.loc[0]['title'])
i = 0

def rename_pdf():

    dir = os.listdir(path_pdf)
    dir = sorted(dir,key=lambda x: os.path.getmtime(os.path.join(path_pdf, x)))
    # print(dir)
    del(dir[0])
    j = 1980
    for i in range(1951,len(dir)):
        file = dir[i].split('_',1)[1]
        # print(file)
        print(file[0])
        if j==2050:
            break
        while file[0]!=art_info.loc[j]['title'][0]:
            j = j+1
        if file[0]==art_info.loc[j]['title'][0]:
            os.rename(path_pdf + '\\' + dir[i], path_pdf + '\\' + str(art_info.loc[j]['art_id']) + '_' + file)
            print(art_info.loc[i]['art_id'])
            print(file)
            j = j+1
        # break


def remove_file(path_pdf,path_file):
    refer_info = pd.read_csv('refer_info.csv', encoding='utf-8')
    dir = os.listdir(path_pdf)
    # print(len(refer_info.nrows))
    for i in range(2050):
        target_pdf = ''
        data = refer_info.loc[refer_info['art_id']==i]
        for file in dir:
            if file.startswith(f'{i}_'):
                target_pdf = file
                print(target_pdf)
                break
        if (len(data)>0 or target_pdf != '') and not os.path.exists(path_file+f'article_{i}'):
            os.mkdir(path_file+f'article_{i}')
            if len(data)>0:
                data.to_csv(path_file+f'article_{i}\\article_info_{i}.csv',index=0)
            if target_pdf != '':
                os.rename(path_pdf + '\\' + target_pdf,path_file+f'article_{i}\{target_pdf}')
            # print(len(data))
        # break


path_pdf = r'D:\PychamProject\数据处理任务\articles'
path_file = r'D:\PychamProject\数据处理任务\articles\\'
remove_file(path_pdf,path_file)