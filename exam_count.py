# -*- coding: utf-8 -*-
"""
Created on Wed May  2 11:59:57 2018
检查数据统计
@author: LiuWeipeng
"""
import numpy as np
import pandas as pd

datas = pd.read_excel(r'D:\文档\smart\医院文档\exam.xlsx')[1:]
equipment = list(datas['设备类型'])
CT_count = equipment.count('CT')
CR_count = equipment.count('CR')
exam_items = list(datas['检查'])
unique_item = list(set(exam_items))
item_count = [exam_items.count(val) for val in unique_item]
result_array = np.vstack([
                             np.array(unique_item),
                             np.array(item_count),
                             np.array(item_count)/len(exam_items)*100
                        ]).T
result_table = pd.DataFrame(result_array, columns=['检查', '频次', '频率'])
result_table['频率'] = result_table['频率'].astype('float32')
result_table['频次'] = result_table['频次'].astype('float32')
sorted_result = result_table.sort_values(by="频率", ascending=False)
sorted_result.to_excel('freq_result.xls', index=None)























