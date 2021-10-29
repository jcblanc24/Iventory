
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

import sys, os

from os import path


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for Pyinstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


from PyQt5.uic import loadUiType

FROM_CLASS, _ = loadUiType(resource_path("main.ui"))

import sqlite3

x = 0
idx = 2


class Main(QMainWindow, FROM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.GET_DATA()
        self.Navigate()

    def Handel_Buttons(self):
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.search_btn.clicked.connect(self.Search)
        self.check_btn.clicked.connect(self.Level)
        self.reset_btn.clicked.connect(self.RESET)
        self.add_btn.clicked.connect(self.ADD)
        self.update_btn.clicked.connect(self.UPDATE)
        self.delete_btn.clicked.connect(self.DELETE)
        self.next_btn.clicked.connect(self.NEXT)
        self.previous_btn.clicked.connect(self.PREVIOUS)
        self.last_btn.clicked.connect(self.LAST)
        self.first_btn.clicked.connect(self.FIRST)

    def GET_DATA(self):

        # Connect to Sqlite3 database add fill GUI table with data.
        conn = sqlite3.connect(resource_path("parts.db"))
        cur = conn.cursor()

        command = ''' SELECT * from parts_table '''
        result = cur.execute(command)

        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # ------------------------------------------------
        cur2 = conn.cursor()
        cur3 = conn.cursor()

        parts_nbr = ''' SELECT COUNT (DISTINCT PartName) from parts_table '''
        reference_nbr = ''' SELECT COUNT (DISTINCT Reference) from parts_table '''

        result_ref_nbr = cur2.execute(reference_nbr)
        result_parts_nbr = cur3.execute(parts_nbr)

        self.lbl_ref_nbr.setText(str(result_ref_nbr.fetchone()[0]))
        self.lbl_parts_nbr.setText(str(result_parts_nbr.fetchone()[0]))

        # ------------------------------------------------------
        cur4 = conn.cursor()
        cur5 = conn.cursor()

        min_hole = ''' SELECT MIN(NumberOfHoles), Reference from parts_table '''
        max_hole = ''' SELECT MAX(NumberOfHoles), Reference from parts_table '''

        result_min_holes = cur4.execute(min_hole)
        result_max_holes = cur5.execute(max_hole)

        r1 = result_min_holes.fetchone()
        r2 = result_max_holes.fetchone()

        self.lbl_min_hole.setText(str(r1[0]))
        self.lbl_max_hole.setText(str(r2[0]))

        self.lbl_min_hole2.setText(str(r1[1]))
        self.lbl_max_hole2.setText(str(r2[1]))

        self.FIRST()
        self.Navigate()

        # ------------------------
        cur6 = conn.cursor()

        command = ''' SELECT * from parts_table '''
        result = cur6.execute(command)
        val = result.fetchone()

        self.id.setText(f'    {str(val[0])}')
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.number_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])

    def Search(self):

        conn = sqlite3.connect("parts.db")
        cur = conn.cursor()

        nbr = int(self.count_filter_txt.text())

        command = ''' SELECT * from parts_table WHERE count<=?'''
        result = cur.execute(command, [nbr])

        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def Level(self):
        conn = sqlite3.connect('parts.db')
        cur = conn.cursor()

        command = ''' SELECT Reference, PartName, Count from parts_table order by Count asc LIMIT 3'''
        result = cur.execute(command)

        self.table2.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def Navigate(self):
        global idx
        conn = sqlite3.connect('parts.db')
        cur = conn.cursor()

        command = ''' SELECT * from parts_table WHERE id=? '''
        result = cur.execute(command, [idx])
        val = result.fetchone()

        self.id.setText(f'    {str(val[0])}')
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.number_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])

    def RESET(self):
        self.id.setText("")
        self.reference.setText("")
        self.part_name.setText("")
        self.min_area.setText("")
        self.max_area.setText("")
        self.number_of_holes.setText("")
        self.min_diameter.setText("")
        self.max_diameter.setText("")
        self.count.setValue(0)

    def ADD(self):
        conn = sqlite3.connect('parts.db')
        cur = conn.cursor()

        reference_ = self.reference.text()
        part_name_ = self.part_name.text()
        min_area_ = self.min_area.text()
        max_area_ = self.max_area.text()
        number_of_holes_ = self.number_of_holes.text()
        min_diameter_ = self.min_diameter.text()
        max_diameter_ = self.max_diameter.text()
        count_ = str(self.count.value())

        row = (reference_, part_name_, min_area_, max_area_, number_of_holes_,
               min_diameter_, max_diameter_, count_)

        command = '''INSERT INTO parts_table(Reference, PartName, MinArea, MaxArea, NumberOfHoles, MinDiameter, 
                    MaxDiameter, Count) VALUES(?,?,?,?,?,?,?,?) '''
        cur.execute(command, row)

        conn.commit()

    def UPDATE(self):
        conn = sqlite3.connect('parts.db')
        cur = conn.cursor()

        id_ = int(self.id.text())
        reference_ = self.reference.text()
        part_name_ = self.part_name.text()
        min_area_ = self.min_area.text()
        max_area_ = self.max_area.text()
        number_of_holes_ = self.number_of_holes.text()
        min_diameter_ = self.min_diameter.text()
        max_diameter_ = self.max_diameter.text()
        count_ = str(self.count.value())

        row = (reference_, part_name_, min_area_, max_area_, number_of_holes_,
               min_diameter_, max_diameter_, count_, id_)

        command = ''' UPDATE `parts_table` SET `Reference` = ?, `PartName` = ?, `MinArea` =?, `MaxArea` = ?, 
                        `NumberOfHoles` = ?, `MinDiameter` = ?, `MaxDiameter` = ?, `Count` = ? WHERE `id` = ? '''
        cur.execute(command, row)

        conn.commit()

    def DELETE(self):
        conn = sqlite3.connect('parts.db')
        cur = conn.cursor()

        id_ = int(self.id.text())

        cur.execute("DELETE FROM `parts_table` WHERE `id` = %d" % id_)
        conn.commit()

    def NEXT(self):
        conn = sqlite3.connect('parts.db')
        cur = conn.cursor()

        command = ''' SELECT id from parts_table '''
        result = cur.execute(command)
        val = result.fetchall()

        tot = len(val)
        global x
        global idx

        x = x + 1
        if x < tot:
            idx = val[x][0]
            self.Navigate()
        else:
            x = tot - 1
            print('End of file')

    def PREVIOUS(self):
        conn = sqlite3.connect('parts.db')
        cur = conn.cursor()

        command = ''' SELECT id from parts_table '''
        result = cur.execute(command)
        val = result.fetchall()

        global x
        global idx

        x = x - 1
        if x > -1:
            idx = val[x][0]
            self.Navigate()
        else:
            x = 0
            print('End of file')

    def LAST(self):
        conn = sqlite3.connect('parts.db')
        cur = conn.cursor()

        command = ''' SELECT id from parts_table '''
        result = cur.execute(command)
        val = result.fetchall()
        tot = len(val)

        global x
        global idx

        x = tot - 1
        if x < tot:
            idx = val[x][0]
            self.Navigate()
        else:
            x = tot - 1
            print('End of file')

    def FIRST(self):
        conn = sqlite3.connect('parts.db')
        cur = conn.cursor()

        command = ''' SELECT id from parts_table '''
        result = cur.execute(command)
        val = result.fetchall()

        global x
        global idx

        x = 0
        if x > -1:
            idx = val[x][0]
            self.Navigate()
        else:
            x = 0
            print('End of file')


def main():
    app = QApplication(sys.argv)
    Window = Main()
    Window.show()
    app.exec_()


if __name__ == '__main__':
    main()
