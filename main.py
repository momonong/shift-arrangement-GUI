import sys
from pandas import read_csv
from os import listdir
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from personnel_data import personnel, filter_by_permission

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('ui_files/login.ui', self)
        self.login_button.clicked.connect(self.fun_login)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def fun_login_check(self, user_name, password):
        try:
            if password==personnel[user_name]['password']:
                print('\nLogin successfully.')
                menu = Menu()
                widget.addWidget(menu)
                widget.setCurrentIndex(widget.currentIndex()+1)
                print(f'\nuser_name = {user_name} \npassword = {password} \npermission = {personnel[user_name]["permission"]}\n')
            else:
                print('\nLogin failed.')
                self.fun_login_fail()
        except KeyError:
            print('\nLogin failed.')
            self.fun_login_fail()

    def fun_login_fail(self):
        login_fail = Login_fail()
        widget.addWidget(login_fail)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def fun_login(self):
        # 使用者的帳號密碼在這
        global user_name 
        user_name = self.user_name.text()
        password = self.password.text()
        self.fun_login_check(user_name, password)

class Login_fail(QDialog):
    def __init__(self):
        super(Login_fail, self).__init__()
        loadUi('ui_files/login_fail.ui', self)
        self.back_login_button.clicked.connect(self.fun_back)

    def fun_back(self):        
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Menu(QDialog):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi('ui_files/menu.ui', self)
        self.first_fun_btn.clicked.connect(self.fun_first)
        if personnel[user_name]['permission'] not in filter_by_permission['lowest_level']:
            self.first_fun_btn.setEnable(False)
        self.sec_fun_btn.clicked.connect(self.fun_second)
        if personnel[user_name]['permission'] not in filter_by_permission['medium_level']: 
            self.sec_fun_btn.setEnabled(False)
        self.third_fun_btn.clicked.connect(self.fun_third)
        if personnel[user_name]['permission'] not in filter_by_permission['highest_level']:
            self.third_fun_btn.setEnabled(False)

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
        self.filename = None
        self.upload_person_btn.clicked.connect(self.fun_check_personal_shift)
        # show 天數統計與 fuzzy logic 所產生之建議 的按鈕
        self.text_btn.clicked.connect(self.fun_show_text)
        self.text_btn_2.clicked.connect(self.fun_confirm_update_shift)
        self.back_btn.clicked.connect(self.fun_back)

    def fun_back(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def fun_check_personal_shift(self):
        self.filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(self.filename, filetype)
        self.path_text.setText(self.filename)
        csv_to_check = read_csv(self.filename, index_col='2023')
        ######################################
        #  這裡 call 檢查排班是否正確的 funcion  
        #  這邊先預設排班正確 return True          
        shift_verified = True
        ######################################
        if shift_verified:
            self.days_cal_text.setText('排班符合規定，確定檔案正確後即可按下「天數統計與建議」按鍵，讓系統檢視、評分')
            self.advise_text.setText('排班符合規定，確定檔案正確後即可按下「天數統計與建議」按鍵，讓系統檢視、評分')
        else:
            self.days_cal_text.setText('排班不符合規定，請調整後再上傳！')
            self.advise_text.setText('排班不符合規定，請調整後再上傳！')

    def fun_show_text(self):
        # 計算特休天數
        self.fun_update_vacation_days()
        ######################################
        #  這裡 call 計算班表 score 的 funcion  
        #  以及 call 生成班表建議的 function
        #  這邊先簡單定義
        score = 100
        advise = 'good'
        ######################################
        # 天數統計與 fuzzy logic 所產生之建議放這裡
        day_cal_text = f'剩下的特休天數：{personnel[user_name]["vacation_days"]} \n\n確認後即可按下「確定上傳」按鍵' 
        advise_text = f'目前班表之分數為分數: {score} \n系統對班表建議: {advise} \n\n確認後即可按下「確定上傳」按鍵'
        self.days_cal_text.setText(day_cal_text)
        self.advise_text.setText(advise_text)
    
    def fun_update_vacation_days(self):
        vacation_days = personnel[user_name]['vacation_days']
        ######################################
        #  這裡 call 計算修了幾天特休的 funcion  
        #  這邊先簡單假設排了兩天特休          
        vacation_days -= 2
        ######################################
        personnel[user_name]['vacation_days'] = vacation_days
        print(f'vacation days: {vacation_days} \npersonnel data: {personnel[user_name]["vacation_days"]}\n')
    
    def fun_confirm_update_shift(self):
        csv_file_df_each = read_csv(self.filename, index_col='2023')
        csv_file_df_all = read_csv('csv_files/_ALL_shift.csv', index_col='2023')
        csv_file_df_each = csv_file_df_each[1:].fillna('')
        csv_file_df_all = csv_file_df_all.fillna('')
        csv_file_df_all = csv_file_df_all.append(csv_file_df_each)
        csv_file_df_all.to_csv('csv_files/_ALL_shift.csv')
        print('\neach person shift:\n', csv_file_df_each)
        print('\nall people shift after merging:\n', csv_file_df_all)

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
        all_csv_file_df = read_csv('csv_files/_ALL_shift.csv', header=None, skiprows=1)
        all_csv_file_df = all_csv_file_df.fillna('')
        print('\nall people shift:\n', all_csv_file_df)
        all_csv_file_df.to_csv('csv_download/all_people_shift.csv')
        # 在連接到資料庫前，先用資料夾的方式進行
        csv_files_each_ls = listdir('csv_files/person_shift')
        if '.DS_Store' in csv_files_each_ls : csv_files_each_ls.remove('.DS_Store')
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
        one_csv_file_df = one_csv_file_df.fillna('')
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
        leave_done_df = leave_done_df.fillna('')
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
        last_done_df = last_done_df.fillna('')
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