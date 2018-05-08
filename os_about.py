# -*- coding: utf-8 -*-
"""
Created on Mon May  7 15:04:26 2018
调用bat,os相关操作
@author: LiuWeipeng
"""

import os
import shutil

os.chdir(r'D:')
os.system('test.bat')

shutil.move('D:/test', 'D:/share')
# shutil.rmtree('d:/dd')

'''
from subprocess import Popen
p = Popen(r"D:\test.bat", cwd=r"D:/")
stdout, stderr = p.communicate()
print(stdout, stderr)

'''
















