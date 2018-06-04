# -*- coding: utf-8 -*-
import pandas as pd
from datetime import timedelta
import numpy as np
import re
import matplotlib.pyplot as plt

def main_time2():
    # df = pd.read_excel(r'D:\文档\smart\医院文档\timeused.xls')

    user_ids = user_id.loc[:, ['F_USER_ID', 'F_USER_TITLE']]
    npd = pd.merge(df, user_ids, on=['F_USER_ID', 'F_USER_ID'], how='left')
    used_time = df.SAVE_TIME - df.LOAD_TIME
    ndf = pd.concat((npd, pd.DataFrame(used_time, columns=['used_time'])), axis=1)
    res1 = pd.DataFrame()
    # res1 = pd.DataFrame(columns=['平均书写时间(分钟)', '最小书写时间(分钟)', '最大书写时间(分钟)'])
    for val in report_writers:
        # print(val)
        # ndf.loc[ndf.isnull(), 'used_time'] = 0
        filter_time = ndf.loc[ndf.F_USER_TITLE == val, 'used_time']

        filter_time[filter_time.isnull()] = 0
        avg_time = filter_time.mean() / timedelta(minutes=1)
        min_time = filter_time.min() / timedelta(minutes=1)
        max_time = filter_time.max() / timedelta(minutes=1)
        sum_time = filter_time.sum() / timedelta(minutes=1)
        time_dic = {'总书写时间(分钟)': sum_time,'平均书写时间(分钟)': avg_time, '最小书写时间(分钟)': min_time, '最大书写时间(分钟)': max_time}
        time_res = pd.DataFrame(data=time_dic, index=[val])
        res1 = pd.concat((res1, time_res), axis=0)
    res2 = signed_df(ndf)
    res = pd.concat((res1, res2), axis=1)

    return res


def signed_df(ndf):
    res = pd.DataFrame(columns=['平均被审核时间(分钟)', '最小被审核时间(分钟)', '最大被审核时间(分钟)'])

    for val in report_writers:
        # print(val)
        main_id_row = ndf.loc[ndf.F_USER_TITLE == val, :]
        no_writer = ndf.loc[ndf.F_USER_TITLE != val, :]
        writer_signer = pd.merge(main_id_row, no_writer, on=['F_MAIN_ID', 'F_MAIN_ID'], how='left')
        filter_time = writer_signer.loc[:, 'used_time_y']
        filter_time[filter_time.isnull()] = 0
        avg_time = filter_time.mean() / timedelta(minutes=1)
        min_time = filter_time.min() / timedelta(minutes=1)
        max_time = filter_time.max() / timedelta(minutes=1)
        time_dic = {'平均被审核时间(分钟)': avg_time, '最小被审核时间(分钟)': min_time, '最大被审核时间(分钟)': max_time}
        time_res = pd.DataFrame(data=time_dic, index=[val])
        res = pd.concat((res,time_res), axis=0)

    return res


def main_time():
    """
    报告书写时间分析，作废
    :return:
    """
    # df = pd.read_excel(r'D:\文档\smart\医院文档\timeused.xls')
    df = pd.read_excel(r'D:\文档\smart\医院文档\前列腺timeused.xlsx')
    user_id = pd.read_excel(r'D:\文档\smart\医院文档\User_id.xlsx')
    user_ids = user_id.loc[:, ['F_USER_ID', 'F_USER_TITLE']]
    npd = pd.merge(df, user_ids, on=['F_USER_ID', 'F_USER_ID'], how='left')
    used_time = df.SAVE_TIME - df.LOAD_TIME
    ndf = pd.concat((npd, pd.DataFrame(used_time, columns=['used_time'])), axis=1)

    res2 = pd.DataFrame(columns=['平均时间(分钟)', '最小时间(分钟)', '最大时间(分钟)'])
    for val in report_signers:
        filter_time = ndf.loc[ndf.F_USER_TITLE == val, 'used_time']
        if len(filter_time) > 0:
            avg_time = filter_time.mean() / timedelta(minutes=1)
            min_time = filter_time.min() / timedelta(minutes=1)
            max_time = filter_time.max() / timedelta(minutes=1)
            time_dic = {'平均时间(分钟)': avg_time, '最小时间(分钟)': min_time, '最大时间(分钟)': max_time}
            time_res = pd.DataFrame(data=time_dic, index=[val])
            res2 = pd.concat((res2,time_res), axis=0)
        # 于磊的日志不存在
    return res2


def get_tnm(diagnosis):
    """
    get tnm
    :param diagnosis:
    :return:
    """
    tnm = []
    for i in range(len(diagnosis)):
        # print(i)

        try:
            # tmp = re.search(r'^(.*)（(T.*?N.*?M.*?)）', diagnosis[i]).group(2)
            tmp = re.search(r'^(.*)(T.*?N.*?M.*?)）', diagnosis[i]).group(2)
            # print(tmp)
        except AttributeError as e:
            # print(i, e)
            tmp = 'TNM'
        tnm.append(tmp)
    return tnm


def tnm_count(report_writers, report_writer, tnm, tnm_columns):
    """
    书写报告的数量
    :param report_writers:
    :param report_writer:
    :param tnm:
    :return:
    """

    res = pd.DataFrame(
                       np.zeros((len(report_writers), len(tnm_columns)), dtype=int),
                       index=report_writers,

                        columns=tnm_columns
                       )
    for i in range(len(tnm)):
        name = report_writer[i]
        if name not in black_list:
            if tnm[i] != 'TNM':
                # print(i)
                tmp = tnm[i]
                tmp = tmp.strip("？")
                # Tx = tmp[:-4]
                t = re.split('N', tmp)
                Tx = t[0]
                t1 = re.split('M', t[1])
                Nx = 'N'+t1[0]
                Mx = 'M'+t1[1]
                # Mx = tmp[-2:]

                # res.loc['王芬', 'T4'] += 1
                # print(tmp)
                exec('res.loc[\'' + name + '\',\'' + Tx + '\'] += 1')
                exec('res.loc[\'' + name + '\',\'' + Nx + '\'] += 1')
                exec('res.loc[\'' + name + '\',\'' + Mx + '\'] += 1')
            else:

                exec('res.loc[\'' + name + '\', \'无TNM\'] += 1')

    return res


def main_count():

    report_writers_counts = [report_writer.count(x) for x in report_writers]
    report_signers_counts = [report_signer.count(x) for x in report_signers]
    diagnosis = list(data_df.F_RPT_DIAGNOSIS)
    tnm = get_tnm(diagnosis)
    tnm_result = tnm_count(report_writers, report_writer, tnm, tnm_column)
    writer_counts = pd.DataFrame(report_writers_counts, index=report_writers, columns=['书写报告总数'])
    signers_counts = pd.DataFrame(report_signers_counts, index=report_signers,columns=['审核报告总数'])

    return tnm_result, writer_counts, signers_counts


def experience():
    data = pd.read_excel(r'D:\文档\smart\医院文档\刘晓飞.xlsx')
    used_time = - (data.LOAD_TIME - data.SAVE_TIME) / timedelta(minutes=1)
    avg_time = []
    for i in range(7):
        if i < 6:
            avg_time.append(used_time[i * 5: (i + 1) * 5].mean())
        else:
            avg_time.append(used_time[i:].mean())
    y=range(7)
    plt.figure(figsize=(8, 4))
    plt.plot(avg_time)
    plt.xlabel("Repeat(every 5)")
    plt.ylabel("Average time(min)")
    plt.show()


if __name__ == "__main__":
    user_id = pd.read_excel(r'D:\文档\smart\医院文档\User_id.xlsx')

    data_df = pd.read_excel(r'D:\文档\smart\医院文档\肾肿瘤+201605-201805.xlsx')
    df = pd.read_excel(r'D:\文档\smart\医院文档\timeused.xls')
    tnm_column = ['T1a', 'T1b', 'T2a', 'T2b', 'T3a', 'T3b', 'T3c', 'T4',
             'N0', 'N1', 'Nx',
             'M0', 'M1', 'Mx', '无TNM']  #肾结石

    # data_df = pd.read_excel(r'D:\文档\smart\医院文档\前列腺诊断原始数据.xlsx')
    # df = pd.read_excel(r'D:\文档\smart\医院文档\前列腺timeused.xlsx')
    # tnm_column = ['T2', 'T2a', 'T2b', 'T2c', 'T3', 'T3a', 'T3b', 'T4',
    #            'N0', 'N1', 'Nx',
    #            'M0', 'M1', 'Mx', 'M1b', '无TNM']  # 前列腺

    black_list = ('测试003', '测试017', '测试020', '测试018', '测试003', '系统管理员')
    report_writer = list(data_df.F_RPT_WRITER)
    report_signer = list(data_df.F_RPT_SIGNER)
    report_writers = list(set(report_writer).difference(black_list))
    report_signers = list(set(report_signer).difference(black_list))
    tnm_res, writer_count, signer_count = main_count()
    writer_signer_time = main_time2()
    signer_time = main_time()
    writer = pd.concat((writer_count, writer_signer_time), axis=1)
    # writer = pd.concat((writer_count, writer_time), axis=1)
    signer = pd.concat((signer_count, signer_time), axis=1)
    tnm_res.to_excel('D:\文档\smart\医院文档\报告医生TNM统计.xls')
    writer.to_excel('D:\文档\smart\医院文档\报告医生时间及份数统计.xls')
    signer.to_excel('D:\文档\smart\医院文档\审核医生时间及份数统计.xls')
    experience()