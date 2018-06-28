# -*- encoding: utf-8 -*-
"""
转换规培表格为规范化形式
"""
import pandas as pd
import os
import re


def gen_df():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = range(2018, 2024)
    columns = []
    for i in years:
        for j in months:
            columns.append(j + str(i))

    indexs = list(NAMES.name)
    df_out = pd.DataFrame(index=indexs, columns=columns)
    return df_out


def get_names(ke):
    names2 = ''
    if type(ke) == str:
        name_list = re.split('\s+', ke)
        names = [x.strip('*') for x in name_list]
        names2 = [x.strip('#') for x in names]
    return names2


def main_talbe():
    df_out = gen_df()
    for i in range(len(df_out.index)):
        for j in range(len(DF)):  # range(6,19)
            for k in range(1, len(DF.columns)):
                ls = DF.iloc[j, k]
                names = get_names(ls)
                if df_out.index[i] in names:
                    # print(df_out.iloc[i, j + 6])
                    if type(df_out.iloc[i, j + 6]) == float:
                        df_out.iloc[i, j + 6] = DF.columns[k]
                    else:
                        df_out.iloc[i, j + 6] += DF.columns[k]
    # df_out.to_excel(os.path.join(FILE_PATH, '轮转计划(自动生成).xlsx'))
    # print('已经输出到：轮转计划(自动生成).xlsx')
    return df_out


def freq(ls):
    dic = ('儿', '胸', '腹', '骨', '核', '介', '超', '急',)
    res = ''
    for val in dic:
        # print(val)
        num = ls.count(val)
        res += val + ':' + str(num) + ';'
    return res


def freqh(ls):
    dic = ('儿', '胸', '腹', '骨', '核', '介', '超', '急',)
    res = ''
    for val in dic:
        # print(val)
        num = ls.count(val)
        res += val + ':' + str(num) + ';\r\n'
    return res


def main():
    df = main_talbe()
    col_sum = []
    for i in range(len(df)):
        ls = list(df.iloc[i, :])
        col = freq(ls)
        col_sum.append(col)
    col_df = pd.DataFrame(data=col_sum, index=df.index, columns=['按人名汇总'])
    ind_sum = []
    for i in range(len(df.columns)):
        ls = list(df.iloc[:, i])
        ind = freqh(ls)
        ind_sum.append(ind)

    ind_df = pd.DataFrame(data=[ind_sum], index=['按月份汇总'], columns=df.columns)
    res = pd.concat((col_df, df), axis=1)
    ress = pd.concat((ind_df, res), axis=0)
    keys = ['按人名汇总']
    keys.extend(df.columns)
    ress = ress[keys]
    ress.to_excel(os.path.join(FILE_PATH, '轮转计划.xlsx'))


if __name__ == '__main__':
    FILE_PATH = os.getcwd()
    FILE_NAME = '住院医排班.xlsx'
    NAME_LIST = '住院医师轮转完成情况.xlsx'
    DF = pd.read_excel(os.path.join(FILE_PATH, FILE_NAME))
    NAMES = pd.read_excel(os.path.join(FILE_PATH, NAME_LIST))
    main()
