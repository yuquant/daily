# -*- coding: utf-8 -*-
"""
Created on Wed May  2 15:29:22 2018
时间统计
@author: LiuWeipeng
"""

import pandas as pd
from datetime import timedelta
datas = pd.read_excel(r'D:\文档\smart\医院文档\exam.xlsx')[1:]

# drop all rows that have any NaN values
clear_data = datas.dropna(axis=0, how='any')
exam_time = list(clear_data['检查时间'])
up_time = list(clear_data['提交时间'])
pass_time = list(clear_data['审核时间'])

equipment = list(clear_data['设备类型'])
CT_count = equipment.count('CT')
CR_count = equipment.count('CR')
print('CT', CT_count, 'CR', CR_count)
exam_items = list(clear_data['检查'])
exam_items = list(clear_data['检查'])
unique_item = list(set(exam_items))
item_count = [exam_items.count(val) for val in unique_item]
freq = [x/len(exam_items)*100 for x in item_count]

# writing_time = [x-y for x in up_time for y in exam_time]
total_writng_time = []
writing_time = []
for j in range(len(unique_item)):
    select_data = clear_data[clear_data.检查 == unique_item[j]]
    use_time = select_data['提交时间']-select_data['检查时间']
    total_time = use_time.sum()/timedelta(days=1)
    avg_time = use_time.sum()/len(use_time)/timedelta(hours=1)
    writing_time.append(avg_time)
    total_writng_time.append(total_time)

total_reading_time = []
reading_time = []
for j in range(len(unique_item)):
    select_data = clear_data[clear_data.检查 == unique_item[j]]
    use_time = select_data['审核时间']-select_data['提交时间']
    total_time = use_time.sum()/timedelta(days=1)
    avg_time = use_time.sum()/len(use_time)/timedelta(hours=1)
    reading_time.append(avg_time)
    total_reading_time.append(total_time)

data_dic = {'检查': unique_item, '频次': item_count, '频率(%)': freq,
            '书写平均时间(小时)': writing_time,
            '审核平均时间(小时)': reading_time,
            '总书写时间(天)': total_writng_time,
            '总审核时间(天)': total_reading_time
            }
result_table = pd.DataFrame(data_dic)
result_table.to_excel('freq_result.xls', index=None)


