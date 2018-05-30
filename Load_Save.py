# -*- coding: utf-8 -*-
import pandas as pd
from datetime import timedelta
import numpy as np
import re


def main_time():
    """
    报告书写时间分析
    :return:
    """
    df = pd.read_excel(r'D:\文档\smart\医院文档\timeused.xls')
    user_id = pd.read_excel(r'D:\文档\smart\医院文档\User_id.xlsx')
    user_ids = user_id.loc[:, ['F_USER_ID', 'F_USER_TITLE']]
    npd = pd.merge(df, user_ids, on=['F_USER_ID', 'F_USER_ID'], how='left')
    used_time = df.SAVE_TIME - df.LOAD_TIME
    ndf = pd.concat((npd, pd.DataFrame(used_time, columns=['used_time'])), axis=1)
    res1 = pd.DataFrame(columns=['平均时间(分钟)', '最小时间(分钟)', '最大时间(分钟)'])
    for val in report_writers:
        filter_time = ndf.loc[ndf.F_USER_TITLE == val, 'used_time']
        avg_time = filter_time.mean() / timedelta(minutes=1)
        min_time = filter_time.min() / timedelta(minutes=1)
        max_time = filter_time.max() / timedelta(minutes=1)
        time_dic = {'平均时间(分钟)': avg_time, '最小时间(分钟)': min_time, '最大时间(分钟)': max_time}
        time_res = pd.DataFrame(data=time_dic, index=[val])
        res1 = pd.concat((res1,time_res), axis=0)

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
    return res1, res2


def get_tnm(diagnosis):
    """
    get tnm
    :param diagnosis:
    :return:
    """
    tnm = []
    for i in range(len(diagnosis)):
        print(i)
        # TODO  TRY TO SOLVE THE PROBLEM WITH REGEX
        try:
            tmp = re.search(r'^(.*)（(T.*?N.*?M.*?)）', diagnosis[i]).group(2)
        except AttributeError as e:
            print(i, e)
            tmp = 'noTNM'
        tnm.append(tmp)
    return tnm


def tnm_count(report_writers, report_writer, tnm):
    """
    书写报告的数量
    :param report_writers:
    :param report_writer:
    :param tnm:
    :return:
    """
    res = pd.DataFrame(
                       np.zeros((len(report_writers), 14), dtype=int),
                       index=report_writers,
                       columns=['T1a', 'T1b', 'T2a', 'T2b', 'T3a', 'T3b', 'T3c', 'T4',
                                'N0', 'N1', 'Nx',
                                'M0', 'M1', 'Mx']
                       )
    for i in range(len(tnm)):
        if tnm[i] != 'noTNM':
            print(i)
            tmp = tnm[i]
            tmp = tmp.strip("？")
            Tx = tmp[:-4]
            Nx = tmp[-4:-2]
            Mx = tmp[-2:]
            name = report_writer[i]
            # res.loc['王芬', 'T4'] += 1

            exec('res.loc[\'' + name + '\',\'' + Tx + '\'] += 1')
            exec('res.loc[\'' + name + '\',\'' + Nx + '\'] += 1')
            exec('res.loc[\'' + name + '\',\'' + Mx + '\'] += 1')

    return res


def main_count():

    report_writers_counts = [report_writer.count(x) for x in report_writers]
    report_signers_counts = [report_signer.count(x) for x in report_signers]
    diagnosis = list(data_df.F_RPT_DIAGNOSIS)
    tnm = get_tnm(diagnosis)
    tnm_result = tnm_count(report_writers, report_writer, tnm)
    writer_counts = pd.DataFrame(report_writers_counts, index=report_writers, columns=['书写报告总数'])
    signers_counts = pd.DataFrame(report_signers_counts, index=report_signers,columns=['审核报告总数'])

    return tnm_result, writer_counts, signers_counts


if __name__ == "__main__":

    data_df = pd.read_excel(r'D:\文档\smart\医院文档\肾肿瘤+201605-201805.xlsx')
    report_writer = list(data_df.F_RPT_WRITER)
    report_signer = list(data_df.F_RPT_SIGNER)
    report_writers = list(set(report_writer))
    report_signers = list(set(report_signer))
    tnm_res, writer_count, signer_count = main_count()
    writer_time, signer_time = main_time()
    writer = pd.concat((writer_count, writer_time), axis=1)
    signer = pd.concat((signer_count, signer_time), axis=1)
    tnm_res.to_excel('D:\文档\smart\医院文档\报告医生TNM统计.xls')
    writer.to_excel('D:\文档\smart\医院文档\报告医生时间及份数统计.xls')
    signer.to_excel('D:\文档\smart\医院文档\审核医生时间及份数统计.xls')