import sys
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('login.ui', self)
        self.login_button.clicked.connect(self.fun_login)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def fun_login(self):
        user_name = self.user_name.text()
        password = self.password.text()
        print(f'\nuser_name = {user_name} \npassword = {password}')
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Menu(QDialog):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi('menu.ui', self)
        self.upload_personal.clicked.connect(self.fun_first)

    def fun_first(self):
        upload_personal = Upload_personal()
        widget.addWidget(upload_personal)
        widget.setCurrentIndex(widget.currentIndex()+1)        
        
class Upload_personal(QDialog):
    def __init__(self):
        super(Upload_personal, self).__init__()
        loadUi('upload_personal.ui', self)
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
        csv_file_df = pd.read_csv(filename, header=None, skiprows=1)
        print(csv_file_df)
    
    def fun_show_text(self):
        print('\ntest\n')
        # 天數統計與 fuzzy logic 所產生之建議放這裡
        day_cal_text = 'testing'
        advise_text = 'testing'
        self.days_cal_text.setText(day_cal_text)
        self.advise_text.setText(advise_text)


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(370)
widget.setFixedWidth(450)
widget.show()
app.exec_()


