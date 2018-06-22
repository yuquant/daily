# -*- encoding:utf-8 -*-
"""
insert nlp to sql server
"""
import pandas as pd
import pyodbc
import time
import os
import re


def exe_db(sql):
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print('success')
    except Exception as e:
        # Rollback in case there is any error
        print(sql)
        print('插入数据失败!', e)

        db.rollback()


def time_gen():
    """
    genarate time str like '2018.06.21 09:18:45'
    :return:
    """
    timestamp = time.time()
    time_local = time.localtime(timestamp)
    res = time.strftime('%Y.%m.%d %H:%M:%S', time_local)
    return res


def date_gen():
    """
    genarate time str like '180621'
    :return:
    """
    timestamp = time.time()
    time_local = time.localtime(timestamp)
    res = time.strftime('%Y%m%d', time_local)
    return res[2:]


def id_gen():
    """
    return the start id
    :return:
    """
    """
    # sql = 'select * from T_SMT_MAIN_TEXT3 where F_MAIN_ID=194601'
    sql = "select top 1 F_ID_END FROM T_SMT_IMPORT_DATA ORDER BY F_DATA_ID DESC;"
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchone()[0] + 1
    """
    res = START_ID
    return res


def recording():
    """
    add a record to the table,update the max num
    """
    record_name = re.split('\.', FILE_NAME)[0]
    sql = """INSERT INTO T_SMT_IMPORT_DATA 
  (F_DATA_NAME,F_DATA_SET,F_IMPORT_TIME,F_ID_BEGIN,F_ID_END)
  VALUES
  ('%s','%s','%s','%s','%s');""" % \
          (record_name, date_gen(), time_gen(), id_gen(), id_gen() + len(DF) - 1)
    exe_db(sql)
    sql = "UPDATE T_SMT_UNIQUE_ID SET F_MAX_ID=%d WHERE F_TAB_ID=1;" % (id_gen() + len(DF) - 1)
    exe_db(sql)


def basic_info(pid, exam_item, exam_date='', gender='', birth='', age=''):
    """
    insert the basic info,like this
    :param pid: from start id to end
    :param exam_date: 20180228
    :param gender: 'F' or 'M"
    :param exam_item: 'CT'
    :param birth:'1938.01.25'
    :param age:'064Y'
    :return:
    """
    sql = """INSERT INTO T_SMT_MAIN_RECORD
    ([F_MAIN_ID]
          ,[F_MAIN_UID]
          ,[F_TYPE_ID]
          ,[F_NEW_TIME]
          ,[F_SEARCH_ID1]
          ,[F_SEARCH_ID2]
          ,[F_SEARCH_ID3]
          ,[F_SEARCH_ID4]
          ,[F_SEARCH_ID5]
          ,[F_SEARCH_ID6]
          ,[F_SPARE_ID1]
          ,[F_SPARE_ID2]
          ,[F_SPARE_ID3]
          ,[F_SPARE_ID4]
          ,[F_SPARE_ID5]
          ,[F_SPARE_ID6]
          ,[F_SPARE_ID7]
          ,[F_SPARE_ID8]
          ,[F_SPARE_ID9]
          ,[F_SPARE_ID10]
          ,[F_SPARE_CHAR1]
          ,[F_SPARE_CHAR2]
          ,[F_SPARE_CHAR3]
          ,[F_SPARE_CHAR4]
    )
    VALUES
    ('%s','%s',1,'%s',1,'%s',2,-11863,-11863,-11863,0,0,0,0,0,0,0,0,0,0,'%s','%s','%s','%s'); """ % \
          (pid, pid, time_gen(), exam_date, gender, exam_item, birth, age)
    # print(sql)
    exe_db(sql)


def exam_info(pid, check_en, check_date=''):
    """

    :param pid:
    :param check_en: '泌尿系CT平扫'
    :param check_date:'2018.04.20'
    :return:
    """
    pid = str(pid)
    sql = """INSERT INTO T_SMT_MAIN_RECORD_EX
(	   [F_MAIN_ID]
      ,[F_SPARE_EX_CHAR1]
      ,[F_SPARE_EX_CHAR2]
      ,[F_SPARE_EX_CHAR5]
      ,[F_SPARE_EX_CHAR6]
      ,[F_SPARE_EX_CHAR7]
      ,[F_SPARE_EX_CHAR8]
      ,[F_SPARE_EX_CHAR11]
)
      VALUES('%s','%s','%s','%s','%s','%s','%s','%s');
    """ % (pid, 'NAME' + pid, 'ID' + pid, check_en, check_date, 'PID' + pid, 'SID' + pid, 'NAME' + pid)
    # print(sql)
    exe_db(sql)


def symptom(pid, sym):
    """

    :param pid:
    :param sym: symptom
    :return:
    """
    sql = """INSERT INTO T_SMT_MAIN_TEXT1
(F_MAIN_ID,F_TEXT,F_SERVER_ID)
VALUES ('%s','%s',0);
    """ % (pid, sym)
    exe_db(sql)


def diagnose(pid, diag):
    sql = """INSERT INTO T_SMT_MAIN_TEXT2
	  (F_MAIN_ID
      ,F_TEXT
      ,F_SERVER_ID)
      VALUES
      ('%s','%s',0)
    """ % (pid, diag)
    exe_db(sql)


def edit_text3(pid, check_item, check_position, institution='北京大学第一医院'):
    """

    :param pid:
    :param check_item: CT
    :param check_position: 头颅CT平扫
    :param institution:
    :return:
    """
    msg = '\r\n\tMainID:%s\r\n\t数据批次:%s\r\n\t检查类型:%s\r\n\t检查部位:%s\r\n\t医疗机构:%s' \
          % (str(pid), date_gen(), check_item, check_position, institution)
    sql = """INSERT INTO T_SMT_MAIN_TEXT3
	(F_MAIN_ID
      ,F_TEXT
      ,F_STATUS_ID
      ,F_RUN_CODE
      ,F_SERVER_ID)
      VALUES('%s','%s',0,0,0);""" % (pid, msg)
    exe_db(sql)


def main():
    # start_id = id_gen()

    #for i in range(20):
    for i in range(len(DF)):
        info = DF.iloc[i, :]
        patient_id = START_ID + i
        item = info.设备类型
        check_name = info.检查
        gender = 'M' if info.性别 == '男' else 'F'
        age = '0' + str(info.年龄).strip('岁') + 'Y' if len(str(info.年龄).strip('岁')) == 2 else str(info.年龄).strip(
            '岁') + 'Y'
        date = info.检查时间
        date1 = date.strftime('%Y%m%d')
        date2 = date.strftime('%Y.%m.%d')
        sym = info.影像学表现
        diag = info.影像学诊断
        basic_info(pid=patient_id, exam_item=item, exam_date=date1, gender=gender, birth='', age=age)
        exam_info(pid=patient_id, check_en=check_name, check_date=date2)
        symptom(pid=patient_id, sym=sym)
        diagnose(pid=patient_id, diag=diag)
        edit_text3(pid=patient_id, check_item=item, check_position=check_name, institution='北京大学第一医院')


if __name__ == "__main__":
    FILE_NAME = '499例急诊泌尿CT平扫v2.xlsx'
    FILE_PATH = r'C:\smart'
    START_ID = 200000
    DF = pd.read_excel(os.path.join(FILE_PATH,FILE_NAME))
    db = pyodbc.connect(r'DRIVER={SQL Server Native Client 10.0};SERVER=127.0.0.1;DATABASE=ppee;UID=sa;PWD=000000')
    recording()
    main()
    # for loop
    db.close()