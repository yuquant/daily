# -*- coding: utf-8 -*-

"""
时间性别分析
"""
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot


def general_analysis(nums_list):
    """
    一般统计值
    nums_list : list of numbers
    """
    time_array = np.array(nums_list)
    time_count = len(nums_list)
    time_mean = time_array.mean()
    time_std = time_array.std()
    time_max = time_array.max()
    time_min = time_array.min()
    time_mid = np.median(time_array)
    print('样本数：%d' % time_count)
    print('均值：%s' % time_mean)
    print('最小值：%s' % time_min)
    print('最大值：%s' % time_max)
    print('标准差：%s' % time_std)
    print('中位数：%s' % time_mid)


def move_bad(nums_list):
    """
    去除异常值
    """
    time_array = np.array(nums_list)
    time_mean = time_array.mean()
    time_std = time_array.std()
    time_array[time_array > time_mean + 3 * time_std] = 200
    plt.bar(range(len(num_list)), time_array)
    plt.show()


def data_sorted(nums_list):
    """
    排序
    """
    time_array = np.array(nums_list)
    time_array.sort()
    plt.bar(range(len(num_list)), time_array)
    plt.show()


def plot_histogram(nums_list, bar_num=800):
    """
    时间间隔频率直方图
    """
    time_array = np.array(nums_list)
    time_mean = time_array.mean()
    time_std = time_array.std()
    time_array[time_array > time_mean + 3 * time_std] = time_mean + 3 * time_std
    pyplot.hist(time_array, bar_num)
    pyplot.xlabel('Minutes')
    pyplot.ylabel('Frequency')
    pyplot.title('Frequency histogram')
    plt.show()


def hours_frequency(file_name):
    """
    时间段统计
    """
    check_time = list(clear_data['检查时间'])
    day_hours = np.zeros(24, dtype=int)
    day_hour = []
    for val in check_time:
        i = val.hour
        day_hours[i] += 1
        day_hour.append(i)

    hour_belong = pd.DataFrame(day_hour,columns=['检查时间点（时）'], index=clear_data.index)
    fi_res = pd.concat((clear_data, used_time,used_time2, hour_belong), axis=1)
    file_path = r'C:\Users\LiuWeipeng\AnacondaProjects\files\%s.xls' % file_name
    fi_res.to_excel(file_path, index=None)

    plt.bar(range(len(day_hours)), day_hours)
    pyplot.xlabel('Hours of a day')
    pyplot.ylabel('Frequency')
    pyplot.title('Examination Frequency histogram')
    plt.show()


def get_head_data():
    """
    获得头颅平扫数据
    :return: DataFrame
    """
    check_items = ['CT颅脑平扫', '头颅CT平扫']
    res = pd.DataFrame(columns=data_df.columns)
    for i in range(len(data_df)):
        if data_df.iloc[i, 6] in check_items:
            res = res.append(data_df.loc[i])
    return res


def get_kidney_data():
    """
    获取泌尿系统统计
    :return: DataFrame
    """
    check_items = ['CT双能泌尿系平扫(肾结石评估)',
                   '泌尿系CT平扫',
                   '泌尿系CT增强',
                   '双能泌尿系CT平扫（肾结石评估）',
                   '双能泌尿系CT平扫（肾结石评估）',
                   'CT泌尿系多期增强'
                   ]
    res = pd.DataFrame(columns=data_df.columns)
    for i in range(len(data_df)):
        symptom = str(data_df.iloc[i, 11])
        if data_df.iloc[i, 6] in check_items and symptom.find('结石') != -1:
                res = res.append(data_df.loc[i])

    return res


def gender_count():
    """
    性别统计
    """
    gender_list = list(clear_data['性别'])
    male = gender_list.count('男')
    female = gender_list.count('女')
    print('男', male, '; 女', female)


def age_hist():
    """
    年龄频率直方图
    """
    print('年龄频率直方图')
    age_list = list(clear_data['年龄'])
    age_int = [int(s.strip('岁')) for s in age_list]
    pyplot.hist(age_int, 100)
    pyplot.xlabel('Ages')
    pyplot.ylabel('Frequency')
    pyplot.title('Ages Frequency histogram')
    plt.show()


if __name__ == "__main__":
    data_df = pd.read_excel(r'C:\Users\LiuWeipeng\AnacondaProjects\files\20180428+急诊影像检查登记项目-匿名后数据 (1).xlsx')
    # result = get_head_data()
    result = get_kidney_data()

    clear_data = result.dropna(axis=0, how='any')

    use_time = (clear_data['提交时间'] - clear_data['检查时间']) / timedelta(minutes=1)
    used_time = pd.DataFrame(use_time, columns=['提交与检查时间差（分钟）'])
    use_time2 = (clear_data['审核时间'] - clear_data['提交时间']) / timedelta(minutes=1)
    used_time2 = pd.DataFrame(use_time2, columns=['审核与提交时间差（分钟）'])
    gender_count()
    print('提交与检查时间差分析')
    num_list = list(use_time)
    general_analysis(num_list)
    move_bad(num_list)
    plot_histogram(num_list,200)
    hours_frequency('kidney')

    print('审核与提交时间差分析')
    num_list = list(use_time2)
    general_analysis(num_list)
    move_bad(num_list)
    plot_histogram(num_list, 200)
    age_hist()