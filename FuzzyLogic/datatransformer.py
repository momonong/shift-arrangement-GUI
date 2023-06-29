import pandas as pd
import numpy as np
import datetime
from  datetime import date
from copy import deepcopy



#可預排休假期:
#1 旅遊+國定假日
A1 = ['國內旅遊','國外旅遊','元旦','228','國慶','清明','端午','中秋','過年','兒童','勞動']
#2 請假
A2 = ['上課','婚假','喪假','病假','公假','產假','事假','育嬰假','家庭照顧假']
#3 例假日(OFF)、特休、休積假 -> AM:200 PM:280 公A:300 公P:380
A3 = ['OFF','102','103','105','AM','207','208','215','PM','公A','315','公P','207','208']

#一般班別排班
B1 = ['73',"73'","84",'95','85',"128",'210',"E",'N','7-11',"84'",'8054','D','D°','PM°','OFF°','271','262','275','護','OFF+']

#手術房
C1 = ['PS','GU','ENT','NS','OBS','GO','GS','CVS','MC','AN']

#上班時長
time = {'AM':4,'207':4,'208':4,'215':4,'PM':4,'公A':4,'315':4,'公P':4,'207':4,'208':4,
        '73':8,"73'":8,"84":8,'95':8,'85':8,"128":8,'210':8,"E":8,'N':8,'7-11':4,
        "84'":8,'8054':8,'D°':8,'PM°':8,'OFF°':8,'262':4,'271':4,'275':4,'護':8}

#加班班別與時長
D1 = ['OFF+','N+','E+','128+','210+','OFF+']
D2 = {'OFF+':8,'N+':8,'E+':8,'128+':8,'210+':8,'OFF+':8}




class PersonalDataTransformer():
    def __init__(self,MemberName:str):
        self.MemberName = MemberName
        self.__ShiftfromUploading = None
        self.ShiftforNationalHoliday = None #personal checking - national holiday checking
    
    #下載template 班表
    def TemplatePersonalShiftforDownload(self):
        #年月份判斷
        today = datetime.date.today()
        year = today.year #民國
        month = today.month
        if month == 12:
           year += 1
           month == 1
        else:
            month += 1 #當月中可以預下個月的班
            
        #日期list
        dayofmonth = [31,28,31,30,31,30,31,31,30,31,30,31]
        if year%4 == 0:
            dayofmonth[1] = 29
        else:
            dayofmonth[1] = 28

        calender = []
        for i in range(dayofmonth[month-1]):
            calender.append(str(i+1))
        #print(f'calender={calender}')

        #星期list
        week = []
        #eng = ['Mon.','Tue.','Wed.','Thu.','Fri.','Sat.','Sun.']
        eng = ['一','二','三','四','五','六','日']
        for j in range(dayofmonth[month-1]):
            thisdate = datetime.date(year,month,j+1)
            weekday = thisdate.weekday()
            week.append(eng[weekday])
        #print(f'week={week}')

        #班表生成
        cal= {str(year):calender,str(month):week,self.MemberName:[np.nan]}
        pd_cal = pd.DataFrame.from_dict(cal,orient='index')
        filename = self.MemberName+'.csv'
        pd_cal.to_csv(filename,header=None,encoding='utf-8-sig')

        return pd_cal

    
    #檢查班表內容是否符合規定，不對的話要再重新上傳
    def CheckifShiftisacceptable(self,FileName:str):
        
        #讀取班表
        name = FileName+'.csv'
        temp = pd.read_csv(name,header=None,index_col=0,encoding='utf-8-sig')
        index = temp.index.to_list()
        print(index)
        for i in index:
            if pd.isna(i):
                temp = temp.dropna(axis=0)
        print(temp)

        #------------- 檢查內容 -------------
        acceptable = A1+A2+A3
        #-----------------------------------
        unacceptable = []
        for i in temp.iloc[2]:
            if pd.isna(i) == False:
                i = i.upper()
                if (i not in acceptable):
                    unacceptable.append(i)
                
        #如有unacceptable -> 跟UI討論
        """要跟UI配合"""
        if len(unacceptable) != 0:
            #self.ShiftfromUploading = None
            print(f'請更正錯誤內容:{unacceptable}後，重新上傳班表。') 
        else:
            return True
    
    #UI:檢查完內容，符合規定的話，上傳已排好的班表
    def UpdatePersonalShift(self,FileName:str):
        name = FileName+'.csv'
        self.__ShiftfromUploading = pd.read_csv(name,header=None,index_col=0,encoding='utf-8-sig')
        index = self.__ShiftfromUploading.index.to_list()
        for i in index:
            if pd.isna(i):
                self.ShiftfromUploading = self.__ShiftfromUploading.dropna(axis=0)


        print(f'已上傳班表')
        
    #回傳已排好的班表
    def ReturnPersonalShift(self)-> pd.DataFrame:
        return self.__ShiftfromUploading
    
    #回傳轉好的班表for 休假天數統計(例假日+國定假日+旅遊/請假/特休)
    def ReturnWorkDayandOff(self):
    
        #-------------國定假日+旅遊-------------
        holiday = A1
        
        #特休
        #1. 半天特休
        yearoff_halfday = ['公A','315','公P']
        #2. 整天特休 : 103 (不用改)

        #例假日
        #1.半天例假日
        weekend_halfday = ['AM','215','PM']
        #2. 整天例假日 : 102、OFF
        weekend = ['102','OFF']

        #半天例假日半天特休: 105

        s = deepcopy(self.__ShiftfromUploading)

        index = 1
        for i in s.iloc[2]:
            if pd.isna(i) == False:
                if i in holiday :
                    s.iloc[2][index] = 'holiday'
                elif i in yearoff_halfday:
                    s.iloc[2][index] = '0.5yearoff'
                elif i == '103':
                    s.iloc[2][index] = 'yearoff'
                elif i in weekend_halfday:
                    s.iloc[2][index] = '0.5OFF'
                elif i.upper() in weekend:
                    s.iloc[2][index] = 'OFF'
                
                index+=1
            else:
                index+=1

        return  s
    

class AllDataTransformer():
    def __init__(self):
        self.__AllShift = None

    def TemplateAllShiftforDownload(self):
        pass
    

    #檢查班表內容是否符合規定，不對的話要再重新上傳
    """還沒完成 要確認班表內容"""
    def CheckifShiftisacceptable(self,FileName:str):

        #讀取班表
        name = FileName+'.csv'
        temp = pd.read_csv(name,header=None,index_col=0,encoding='utf-8-sig')
        index = temp.index.to_list()
        for i in index:
            if pd.isna(i):
                temp = temp.dropna(axis=0)

        #----------- 檢查內容 -----------
        acceptable = A1+A2+A3+B1
        #-------------------------------

        unacceptable_name = []
        unacceptable_shift = []
        for i in range(2,temp.shape[0]):
            name = temp.index.to_list()[i]
            shift = []
            for j in range(temp.shape[1]):
                s = str(temp.iat[i,j]).upper()
                if (s not in acceptable):
                    shift.append(s)
                    if name not in unacceptable_name:
                        unacceptable_name.append(name)
            if name in unacceptable_name:
                unacceptable_shift.append(shift)
            

        if len(unacceptable_name) != 0:
            print('請更正以下錯誤內容後，重新上傳')
            for i in range(len(unacceptable_name)):
                print(f'{i+1}. {unacceptable_name[i]} : {unacceptable_shift[i]}\n')
        else:
            print('班表符合規定')
            return True
    
    #上傳已排好的班表
    def UpdateAllshift(self,filename:str):
        name = filename+'.csv'
        self.__AllShift = pd.read_csv(name,header=None,index_col=0,encoding='utf-8-sig')
        index = self.__AllShift.index.to_list()
        for i in index:
            if pd.isna(i):
                self.__AllShift = self.__AllShift.dropna(axis=0)

        print(f'已上傳班表')
        """
        
        ========================================
               0  |  1  |  2  |  3  |  4  |  5...
        ========================================
        2023 |             日期
        ----------------------------------------
        month|             星期
        ---------------------------------------
        編號1|          排假日+班別
        ---------------------------------------
        編號2|          排假日+班別
        ...

        """

    #回傳已排好的班表
    def ReturnAllShift(self):
        return self.__AllShift
        
    #回傳一般班別人員檢測所需要的班表
    def DictionaryforNumberofShift(self) -> dict:
        #從全班表找各個班別的人數
        #row 2 開始 為每人的班表
        AllShift = deepcopy(self.__AllShift)

        #------班表-----
        data = {'73':[],"73'":[],"84":[],'95':[],'85':[],"128":[],'210':[],"E":[],'N':[]}
        #---------------
        col =[]
        for i in range(AllShift.shape[1]): #每日為單位算人數
            week = AllShift.iat[1,i]
            col.append(week)
            tmpdict={'73':0,"73'":0,"84":0,'95':0,'85':0,"128":0,'210':0,"E":0,'N':0} #儲存每日各班別的人數
            for j in range(2,AllShift.shape[0]):
                shiftname = AllShift.iat[j,i] #班別
                if shiftname in tmpdict:
                    tmpdict[shiftname] += 1
            for e in tmpdict:
                number = tmpdict.get(e)
                data[e].append(number)

        final = pd.DataFrame.from_dict(data,orient='index',columns=col)
        
        return final
    
    #回傳手術房人員檢測所需的班表
    def ArrayforNumberofOperationRoom(self) -> list:
        #從全班表找各個班別的人數
        #row 2 開始 為每人的班表

        #ENT 五官科 ; MC 控台 ; AN 副護理長
        #週一~週六 每日手術需求人數
        AllShift = deepcopy(self.__AllShift)
        operationroom = {'PS':[0,0,0,0,0,0],'GU':[0,0,0,0,0,0],'ENT':[0,0,0,0,0,0],
                         'NS':[0,0,0,0,0,0],'OBS':[0,0,0,0,0,0],'GO':[0,0,0,0,0,0],
                         'GS':[0,0,0,0,0,0],'CVS':[0,0,0,0,0,0],'MC':[0,0,0,0,0,0],'AN':[0,0,0,0,0,0]}
        final_numberofshift = []

        #weekindex = {'Mon.':0,'Tue.':1,'Wed.':2,'Thu.':3,'Fri.':4,'Sat.':5,'Sun.':6}
        weekindex = {'一':0,'二':1,'三':2,'四':3,'五':4,'六':5,'日':6}

        tmp_operation = deepcopy(operationroom)
        for i in range(AllShift.shape[1]):
            week  = AllShift.iat[1,i]
            for j in range(2,AllShift.shape[0]):
                tmpname = AllShift.iat[j,i] #班別名稱
                if tmpname in operationroom:
                    #print(tmpname,week)
                    index_week = weekindex[week]
                    tmp_operation[tmpname][index_week] += 1

            if week == '日':
                final_numberofshift.append(tmp_operation)
                tmp_operation = deepcopy(operationroom)

        return final_numberofshift
    
    #回傳做六休一/上班天數統計所需要的班表
    """請假先跳過"""
    def DataFrameforSixDutyOneFree(self) -> pd.DataFrame:
        shift = deepcopy(self.__AllShift)
        on = B1+D1+['上課','公假','AM','207','208','215','PM','公A','315','公P'] #全日上班+半日上班
        off = ['OFF','102','103','105']+A1 #全日放假
        shift_for_mark = deepcopy(self.__AllShift) #用來標註有問題之班表

        for i in range(2,shift.shape[0]):
            for j in range(shift.shape[1]):
                tmp = shift.iat[i,j]        
                if tmp.upper() in on:
                    shift.iat[i,j] = 'on'
                elif tmp.upper() in off:
                    shift.iat[i,j] = 'off'
                    
        return shift,shift_for_mark



    #回傳每日可休人數檢測所需要的班表
    def listforPerDayOff(self) -> list :
        
        #NumberofPerDayOff = {'Mon.':0,'Tue.':0,'Wed.':0,'Thu.':0,'Fri.':0,'Sat.':0,'Sun.':0}
        NumberofPerDayOff = {'一':0,'二':0,'三':0,'四':0,'五':0,'六':0,'日':0}
        AllShift = deepcopy(self.__AllShift)

        tmpperday = deepcopy(NumberofPerDayOff)
        finalPerdayOff = []
        acceptable = A1+A2+A3
        for j in range(AllShift.shape[1]):
            for i in range(2,AllShift.shape[0]):
                week  = AllShift.iat[1,j]
                tmp = AllShift.iat[i,j] #班別名稱
                if tmp.upper() in acceptable:
                    tmpperday[week] += 1
            if week == '日':
                finalPerdayOff.append(tmpperday)
                tmpperday = deepcopy(NumberofPerDayOff)


        return finalPerdayOff 

    #回傳例假日檢測(加班統計/公假)所需要的班表
    """請假先跳過(除了公假)"""
    def DataFrameforweekend(self) -> pd.DataFrame:
        AllShift = deepcopy(self.__AllShift)
        shift_for_mark = deepcopy(self.__AllShift)#用來標註有問題之班表
        #全日上班
        on = B1+D1+['公假'] 
        #半日上班
        on2 = ['AM','207','208','215','PM','公A','315','公P']
        #全日放假
        off = A1+['OFF','102','103','105']
        #公假
        occup = ['上課']
        for i in range(2,AllShift.shape[0]):
            for j in range(AllShift.shape[1]):
                tmp = AllShift.iat[i,j]
                if tmp.upper() in on :
                    AllShift.iat[i,j] = 'on'
                elif tmp.upper() in on2 :
                    AllShift.iat[i,j] = 'on2'
                elif tmp.upper() in off :
                    AllShift.iat[i,j] = 'off'
        return AllShift,shift_for_mark

        
        
    