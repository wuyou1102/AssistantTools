# -*- encoding:UTF-8 -*-
import xlwt
import time
from ExcelStyle import ExcelStyle


class Workbook(object):
    def __init__(self, save_path, titles):
        self.__path = save_path
        self.__book = xlwt.Workbook()
        self.__sheet = self.__book.add_sheet(u"数据记录")
        self.__data_style = ExcelStyle.cell_style(font_size=13, font_color=0)
        self.__title_style = ExcelStyle.cell_style(font_size=14, font_color=0)
        self.__row = self.__yield_row()
        self.__init_sheet_title(titles)

    def __init_sheet_title(self, title):
        row = self.__row.next()
        self.__sheet.write(row, 0, u"时间", self.__title_style)
        self.__sheet.set_col_default_width(100)
        for i in range(len(title)):
            col = i + 1
            self.__sheet.write(row, col, title[i], self.__title_style)
        self.save()

    def write_row(self, *args):
        row = self.__row.next()
        self.__sheet.write(row, 0, self.__timestamp(), self.__data_style)
        for i in range(len(args)):
            col = i + 1
            self.__sheet.write(row, col, args[i], self.__data_style)
        self.save()

    def __yield_row(self):
        row = 0
        while True:
            yield row
            row += 1

    def save(self):
        try:
            self.__book.save(self.__path)
        except IOError:
            pass

    @staticmethod
    def __timestamp():
        return time.strftime('%H:%M:%S', time.localtime(time.time()))
