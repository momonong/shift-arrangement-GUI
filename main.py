import sys
from pandas import read_csv
from os import listdir
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('ui_files/login.ui', self)
        self.login_button.clicked.connect(self.fun_login)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def fun_login(self):
        # 使用者的帳號密碼在這
        user_name = self.user_name.text()
        password = self.password.text()
        print(f'\nuser_name = {user_name} \npassword = {password}')
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Menu(QDialog):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi('ui_files/menu.ui', self)
        self.first_fun_btn.clicked.connect(self.fun_first)
        self.sec_fun_btn.clicked.connect(self.fun_second)
        self.third_fun_btn.clicked.connect(self.fun_third)

    def fun_first(self):
        upload_person = Upload_person()
        widget.addWidget(upload_person)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def fun_second(self):
        check_all_shift = Check_all_shift()
        widget.addWidget(check_all_shift)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def fun_third(self):
        check_last_shift = Check_last_shift()
        widget.addWidget(check_last_shift)
        widget.setCurrentIndex(widget.currentIndex()+1)         
        
class Upload_person(QDialog):
    def __init__(self):
        super(Upload_person, self).__init__()
        loadUi('ui_files/upload_person.ui', self)
        self.upload_person_btn.clicked.connect(self.fun_upload_person)
        self.text_btn.clicked.connect(self.fun_show_text)
        # show 天數統計與 fuzzy logic 所產生之建議 的按鈕
        self.back_btn.clicked.connect(self.fun_back)

    def fun_back(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def fun_upload_person(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(filename, filetype)
        self.path_text.setText(filename)
        # 上傳的個人班表在這
        # csv_file_df 裡的 df 已經去除掉 header 
        csv_file_df = read_csv(filename, header=None, skiprows=1)
        print('\neach person shift:\n', csv_file_df)
    
    def fun_show_text(self):
        # 天數統計與 fuzzy logic 所產生之建議放這裡
        day_cal_text = 'testing'
        advise_text = 'testing'
        self.days_cal_text.setText(day_cal_text)
        self.advise_text.setText(advise_text)

class Check_all_shift(QDialog):
    def __init__(self):
        super(Check_all_shift, self).__init__()
        loadUi('ui_files/check_all_shift.ui', self)
        self.back_btn.clicked.connect(self.fun_back)
        self.download_all_btn.clicked.connect(self.fun_download_all)
        self.download_one_btn.clicked.connect(self.fun_download_one)

    def fun_back(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def fun_download_all(self):
        # 整理過後的所有人班表會在這個 csv 檔裡面
        all_csv_file_df = read_csv('csv_files/ALL_shift.csv', header=None, skiprows=1)
        print('\nall people shift:\n', all_csv_file_df)
        all_csv_file_df.to_csv('csv_download/all_people_shift.csv')
        # 在連接到資料庫前，先用資料夾的方式進行
        csv_files_each_ls = listdir('csv_files/person_shift')
        csv_files_each = ''
        for i in csv_files_each_ls:
            csv_files_each += i+'\n'
        self.show_all_file_text.setText(csv_files_each)

    def fun_download_one(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "csv_files/person_shift")                 # start path
        print(filename, filetype)
        # 可以從這裡挑選特定某個人的班表
        one_csv_file_df = read_csv(filename, header=None, skiprows=1)
        print('\nspecific person shift:\n', one_csv_file_df)
        one_csv_file_df.to_csv('csv_download/specific_person_shift.csv')

class Check_last_shift(QDialog):
    def __init__(self):
        super(Check_last_shift, self).__init__()
        loadUi('ui_files/check_last_shift.ui', self)
        self.back_btn.clicked.connect(self.fun_back)
        self.download_leave_btn.clicked.connect(self.fun_download_leave) 
        self.upload_last_btn.clicked.connect(self.fun_upload_last) 
        self.advice_btn.clicked.connect(self.fun_show_advice)

    def fun_back(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def fun_download_leave(self):
        # 排假過後的班表會存在這個 df 裡面
        leave_done_df = read_csv('csv_files/leave_done.csv', header=None, skiprows=1)
        print('\nafter leave arrangement shift:\n', leave_done_df)
        leave_done_df.to_csv('csv_download/after_leave_arrangement_shift.csv')

    def fun_upload_last(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(filename, filetype)
        self.show_path_text.setText(filename)
        # 上傳的最後排班完成之班表在這
        last_done_df = read_csv(filename, header=None, skiprows=1)
        print('\nlast all done shift:\n', last_done_df)

    def fun_show_advice(self):
        # 系統對於排班後之整份班表的回饋與建議 放這裡
        advise_text = 'testing'
        self.show_advice_text.setText(advise_text)

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(370)
widget.setFixedWidth(450)
widget.show()
app.exec_()