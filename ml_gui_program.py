from turtle import st
from PyQt5.QtWidgets import *
import sys,pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from data_visualise import data_
from table_display import DataFrameModel
from add_steps import add_steps

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('mainwindow.ui' , self)

        global data, steps
        data = data_()
        steps = add_steps()

        self.browse_btn = self.findChild(QPushButton, "browse_btn")
        self.submit_btn = self.findChild(QPushButton, "submit_btn")
        self.convert_btn = self.findChild(QPushButton, "convert_btn")
        self.drop_btn = self.findChild(QPushButton, "drop_btn")
        self.fill_mean_btn = self.findChild(QPushButton, "fill_mean_btn")
        self.fillna_btn = self.findChild(QPushButton, "fillna_btn")
        self.columns = self.findChild(QListWidget, "column_list")
        self.table = self.findChild(QTableView, "tableView")
        self.data_shape = self.findChild(QLabel, "shape")
        self.label_2 = self.findChild(QLabel, "label_2")
        self.target_col = self.findChild(QLabel, "target_col")
        self.cat_column = self.findChild(QComboBox, "cat_column")
        self.drop_column = self.findChild(QComboBox, "drop_column")
        self.empty_column = self.findChild(QComboBox, "empty_column")

        self.browse_btn.clicked.connect(self.getCSV)
        self.columns.clicked.connect(self.target)
        self.submit_btn.clicked.connect(self.set_target)
        self.convert_btn.clicked.connect(self.con_cat)
        self.drop_btn.clicked.connect(self.dropc)
        self.fill_mean_btn.clicked.connect(self.fillmean)
        self.fillna_btn.clicked.connect(self.fillna)

    def filldetails(self, flag = 1):
        if flag == 0 :
            self.df = data.read_file(str(self.filepath))

        self.columns.clear()
        self.columns_list = data.get_column_list(self.df)
        print(self.columns_list)

        for i, j in enumerate(self.columns_list):
            # print(i, j)
            stri = f'{j}--{str(self.df[j].dtype)}'
            # print(stri)
            self.columns.insertItem(i, stri)

        x, y = data.get_shape(self.df)
        self.data_shape.setText(f'({x},{y})')
        self.fill_combo_box()


    def fill_combo_box(self):

        self.cat_column.clear()
        self.cat_column.addItems(self.columns_list)
        self.drop_column.clear() 
        self.drop_column.addItems(self.columns_list)
        self.empty_column.clear() 
        self.empty_column.addItems(self.columns_list)
        x = DataFrameModel(self.df)
        self.table.setModel(x)


    def getCSV(self):
        self.filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "./")
        self.columns.clear()
        print(self.filepath)
        if self.filepath != "":
            self.filldetails(0)

    def target(self):
        self.item = self.columns.currentItem()


    def set_target(self):
        self.target_value = str(self.item.text()).split('--')[0]
        # print(self.target_value)
        steps.add_code(f"target=data[{self.target_value}]")
        self.target_col.setText(self.target_value)

    
    def con_cat(self):
        selected = self.cat_column.currentText()
        # print(selected)
        self.df[selected], func_name = data.convert_category(self.df, selected)
        steps.add_text("Column "+ selected + " converted using LabelEncoder")
        steps.add_pipeline("LabelEncoder",func_name)
        self.filldetails()

    def dropc(self):
        selected = self.drop_column.currentText()
        steps.add_code("data=data.drop('"+self.drop_column.currentText()+"',axis=1)")
        steps.add_text("Column "+ self.drop_column.currentText()+ " dropped")
        self.df = data.drop_columns(self.df, selected)
        self.filldetails()

    def fillmean(self):
        selected = self.empty_column.currentText()
        type = self.df[selected].dtype
        if type != 'object':
            self.df[selected] = data.fillmean(self.df, selected)
            self.filldetails()
            # print('not object!')
        else:
            print('dataypte is object!')


    def fillna(self):
        selected = self.empty_column.currentText()
        self.df[selected] = data.fillna(self.df, selected)
        self.filldetails()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window=UI()
    window.show()

    sys.exit(app.exec_())