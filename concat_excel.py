# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:23:07 2018
liushui
@author: LiuWeipeng
"""
import pandas as pd
import os


'''
单个文件
'''


def single_out(in_path):
    tables = pd.read_excel(in_path)
    if len(str(tables.iloc[0, 3])) == 7:
        tables.iloc[:, 3] = tables.iloc[:, 3].map(lambda x: 'A00'+str(x))
    elif len(str(tables.iloc[0, 3])) == 8:
        tables.iloc[:, 3] = tables.iloc[:, 3].map(lambda x: 'A0'+str(x))
    tables.to_excel('result.xls')

if __name__ == "__main__":
    input_dirs = r"F:\gulingyuan"
    dirs = os.listdir(input_dirs)
    for i in range(len(dirs)):
        filedirs = os.path.join(input_dirs, dirs[i])
        files = os.listdir(filedirs)
        if i == 0:
            tables = pd.read_excel(os.path.join(input_dirs, dirs[i], files[0]))
        else:
            tmp = pd.read_excel(os.path.join(input_dirs, dirs[i], files[0]))
            tables = pd.concat((tables, tmp), axis=0)
    tables.iloc[:, 3] = tables.iloc[:, 3].map(lambda x: 'A00'+str(x))
    tables.to_excel('result.xls')

    # single_out(r"D:\文档\smart\医院文档\张一帆.xls")
