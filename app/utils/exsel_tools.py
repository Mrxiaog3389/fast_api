# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
import pandas as pd
import numpy as np
from io import BytesIO
import time,datetime

class ExcelTools:

    def dict_to_excel(self, datas,columns):
        # 创建数据流
        output = BytesIO()
        # 创建excel work book
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        workbook = writer.book
        # 创建excel sheet
        worksheet = workbook.add_worksheet('sheet1')
        # cell 样式
        cell_format = workbook.add_format({
            'border': 1,
            'align': 'center',
        })
        col = 0
        for item in columns:
            worksheet.write(0, col, item, cell_format)
            col += 1
        # 写入数据
        for row in range(1, len(datas)+1):
            for col in range(0, len(datas[row-1])):
                worksheet.write(row, col, datas[row-1][col], cell_format)
        if len(columns) == 14:
            for row in range(1, len(datas)+1):
                time1 = int(time.mktime(datas[row-1][13].timetuple()))
                time2 = datetime.datetime.fromtimestamp(time1)
                date = "%s-%s-%s" % (time2.year, time2.month, time2.day)
                worksheet.write(row, 13, date, cell_format)
        else:
            for row in range(1, len(datas)+1):
                time1 = int(time.mktime(datas[row-1][14].timetuple()))
                time2 = datetime.datetime.fromtimestamp(time1)
                date = "%s-%s-%s" % (time2.year, time2.month, time2.day)
                worksheet.write(row, 14, date, cell_format)
        worksheet.set_column('A:N', 18)
        writer.close()
        output.seek(0)
        return output

