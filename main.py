import sys
from pandas import read_csv
from os import listdir
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('ui/login.ui', self)
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
        loadUi('ui/menu.ui', self)
        self.first_fun_btn.clicked.connect(self.fun_first)
        self.sec_fun_btn.clicked.connect(self.fun_second)

    def fun_first(self):
        upload_personal = Upload_personal()
        widget.addWidget(upload_personal)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def fun_second(self):
        check_all_shift = Check_all_shift()
        widget.addWidget(check_all_shift)
        widget.setCurrentIndex(widget.currentIndex()+1)        
        
class Upload_personal(QDialog):
    def __init__(self):
        super(Upload_personal, self).__init__()
        loadUi('ui/upload_personal.ui', self)
        self.upload_personal_btn.clicked.connect(self.fun_upload_personal)
        self.text_btn.clicked.connect(self.fun_show_text)
        # show 天數統計與 fuzzy logic 所產生之建議 的按鈕
        self.back_btn.clicked.connect(self.fun_back)

    def fun_back(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def fun_upload_personal(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(filename, filetype)
        self.path_text.setText(filename)
        # 上傳的個人班表在這
        # csv_file_df 裡的 df 已經去除掉 header 
        csv_file_df = read_csv(filename, header=None, skiprows=1)
        print(csv_file_df)
    
    def fun_show_text(self):
        # 天數統計與 fuzzy logic 所產生之建議放這裡
        day_cal_text = 'testing'
        advise_text = 'testing'
        self.days_cal_text.setText(day_cal_text)
        self.advise_text.setText(advise_text)

class Check_all_shift(QDialog):
    def __init__(self):
        super(Check_all_shift, self).__init__()
        loadUi('ui/check_all_shift.ui', self)
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
        print(all_csv_file_df)
        # 在連接到資料庫前，先用資料夾的方式進行
        csv_files_each_ls = listdir('csv_files')
        csv_files_each_ls.remove('ALL_shift.csv')
        csv_files_each = ''
        for i in csv_files_each_ls:
            csv_files_each += i+'\n'
        self.show_all_file_text.setText(csv_files_each)

    def fun_download_one(self):
        filename_one, filetype_one = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "csv_files")                 # start path
        print(filename_one, filetype_one)
        # 可以從這裡挑選特定某個人的班表
        one_csv_file_df = read_csv(filename_one, header=None, skiprows=1)
        print(one_csv_file_df)


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(370)
widget.setFixedWidth(450)
widget.show()
app.exec_()