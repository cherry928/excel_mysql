#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import xlrd
import mysql.connector
from common.config_utils import config
from common.log_utils import logger

def read_excel_data_into_mysql_database(excel_path):
    try:
        workbook = xlrd.open_workbook(excel_path)
        logger.info('创建workbook对象成功')
    except FileNotFoundError as e:
        current_path = os.path.dirname(__file__)
        excel_path = os.path.join(current_path, '../data/stu_info.xlsx')
        workbook = xlrd.open_workbook(excel_path)
        logger.error('excel文件未找到，使用默认路径文件：%s' % excel_path)
    sheet = workbook.sheet_by_index(0)
    cnx = mysql.connector.connect(user=config.get_mysql_user, password=config.get_mysql_password,
                                  host=config.get_mysql_host,
                                  database=config.get_mysql_database)
    for i in range(1, sheet.nrows):
        case_info = []
        for j in range(sheet.ncols):
            if 'time' in str(sheet.cell_value(0, j)):
                # 处理日期为日期格式
                case_info.append(xlrd.xldate.xldate_as_datetime(sheet.cell_value(i,j),0).strftime('%Y-%m-%d %H:%M:%S'))
            elif 'int' in str(sheet.cell_value(0, j)):
                # 处理期数、工号、推广组、城市为整形
                case_info.append(int(sheet.cell_value(i ,j)))
            elif 'null' in str(sheet.cell_value(0, j)):
                case_info.append('NULL')
            else:
                case_info.append(sheet.cell_value(i, j))
        cursor = cnx.cursor()
        sql = "insert into joycloud_f_dt_platform_data_lines" \
              "( uid, ord_no, fst_int_dte, stg_typ, bsy_typ, emp_no, emp_nam, tem_id, tem_nam, cty_id, cty_nam, fst_ord, cus_nam, rpt_cus_nam, lft_prc_amt, min_ovd_dte, max_ovd_stt, ovd_fst_stg_no)" \
              " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%tuple(case_info)
        print(sql)
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
    cnx.close()

if __name__=='__main__':
    cases = read_excel_data_into_mysql_database(config.get_excel_path)
    print(cases)