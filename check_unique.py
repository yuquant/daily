# -*- coding: utf-8 -*-
"""
Created on Sun May  8 08:56:27 2016
check unique
@author: admin
"""

import pandas as pd
import os
'''
old files
'''
old_dirs = (
            'D:\\xiaodong\\data\\test\\20180423',
            r'D:\xiaodong\data\test\20180424',
            r'D:\xiaodong\data\test\20180502',
            r'D:\xiaodong\data\test\2008008_50_samples',
            )
old_list = []
for val in old_dirs:
    tmp_files = os.listdir(val)
    old_list.extend(tmp_files)

print(len(old_list)-len(set(old_list)), 'repeated;', len(old_list), 'total')

'''
new files
'''
new_dirs = (
            r'D:\liuweipeng\others\20180506+深睿P07-肺结节-第四批86例-项目2018008.xlsx',
            r'D:\liuweipeng\others\20180502+深睿P07-肺结节-第四批21例-项目2018008.xlsx',
            r'D:\liuweipeng\others\20180503+深睿P07-肺结节-第四批46例-项目2018008.xlsx',
            r'D:\liuweipeng\others\20180504+深睿P07-肺结节-第四批32例-项目2018008.xlsx',
            r'D:\liuweipeng\others\20180505+深睿P07-肺结节-第四批31例-项目2018008.xlsx',
            )

new_list = []
for val in new_dirs:
    tmp_list = pd.read_excel(val, header=None)
    new_list.extend(list(tmp_list.iloc[:, 0]))

a_codes = list(set(new_list))

'''
is history unique
'''
all_list = []
all_list.extend(old_list)
all_list.extend(a_codes)
print(len(all_list)-len(set(all_list)), 'repeated;', len(all_list), 'total')

'''
output to txt and cfg
'''

if len(new_list) == len(a_codes):
    file = open(r'D:\liuweipeng\others\name.txt', 'w')
    for val in a_codes:
        file.write(val+'\n')
    file.close()
    print(len(a_codes), 'finished')

    with open(r'D:\liuweipeng\others\download.cfg', 'w') as f:
        '''
        change directory
        '''
        config = "[Options]\njavahome = C:\\Program Files (x86)\\Java\\jre6\
        \noutputpath = D:\\xiaodong\\data\\test\\20180502\npausetime = 600"
        f.write(config)
else:
    print(len(new_list)-len(a_codes), 'repeated')
    check_list = []
    repeated_list = []
    for val in new_list:
        if val not in check_list:
            check_list.append(val)
        else:
            repeated_list.append(val)
    print(repeated_list)
