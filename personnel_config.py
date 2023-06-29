#1 特休天數（一年重新計算一次）
#2 修過的國定假日（年份+名稱 例如 112端午）
#3 職稱
#4 請假日期（要分假別） （一年重新計算一次）

# 理論上這邊應該是抓取資料庫內的資料
# 先在這裡定義每個人預設的特休天數 = 8
vacation_days = 8
# 修過的國定假日
national_holidays = '112端午'
# 職稱
position = ['boss', 'manager', 'staff']
# 請假日期 + 假別
leave_date = {
    # 假別
    'ls_leave_kind' : ['事假', '病假', '喪假', '生理假', '公假'],
    # 開始日期
    'leave_start_date' : '112/6/15',
    # 結束日期
    'leave_end_date' : '112/6/17'
}
# 先以字典方式代替資料庫
personnel = {
    'Jonny': {
        'password': 'jonny', 
        'position': position[0],
        'vacation_days': vacation_days},

    'KUMA': {
        'password': 'kuma', 
        'permission': position[1],
        'vacation_days': vacation_days},

    'Morris': {
        'password': 'morris', 
        'permission': position[2],
        'vacation_days': vacation_days},
}
# 以字典方式紀錄不同功能的權限
filter_by_permission = {
    'highest_level': ['boss'],
    'medium_level': ['boss', 'manager'],
    'lowest_level': ['boss', 'manager', 'staff']
}