# -*- coding: utf-8 -*-
"""
Created on Tue May  8 10:40:29 2018
multiprocess
@author: LiuWeipeng
"""
from multiprocessing import Process
import os
import dicom
from time import time


def anyomus(in_dirs, output_dirs):

    for i in range(len(in_dirs)):
        filedirs = os.path.join(r"D:\文档\smart\医院文档\dicom图像\20180502",
                                in_dirs[i])
        files = os.listdir(filedirs)
        for j in range(len(files)):
            ds = dicom.read_file(os.path.join(filedirs, files[j]))
            if len(ds.AccessionNumber) == 7:
                ds.AccessionNumber = 'A00'+ds.AccessionNumber
                if os.path.exists(os.path.join(output_dirs, in_dirs[i])):
                    pass
                else:
                    os.mkdir(os.path.join(output_dirs, in_dirs[i]))
                ds.save_as(os.path.join(output_dirs,
                                        in_dirs[i], files[j]))
            else:
                print(ds.AccsessionNumber)
        percent = round(i/len(in_dirs)*100, 2)
        print(str(percent)+' %')

if __name__ == "__main__":
    output_dirs = r"D:\文档\smart\医院文档\dicom图像\changes"
    dirs = os.listdir(r"D:\文档\smart\医院文档\dicom图像\20180502")
    cores = 4  # cores of computer
    # test = []
    t1 = time()
    if not os.path.exists(output_dirs):
        os.mkdir(output_dirs)
    sep = int(len(dirs)/cores)
    for i in range(cores):
        if i != cores-1:
            in_dirs = dirs[i * sep: (i+1) * sep]
        else:
            in_dirs = dirs[i * sep:]
        # test.extend(in_dirs)
    # print(len(set(test)))
        pro = Process(target=anyomus, args=(in_dirs, output_dirs))
        pro.start()
        #pro.join()
    t2 = time()
    passby = (t2-t1)/60
    print('finished,time used %d minutes' % (passby))
