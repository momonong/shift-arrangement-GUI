# 先在這裡定義每個人預設的特休天數 = 8
# 理論上這邊應該是抓取資料庫內的資料
vacation_days = 8

# 先以字典方式代替資料庫
personnel = {
    'Jonny': {
        'password': 'jonny', 
        'permission': 'boss',
        'vacation_days': vacation_days},

    'KUMA': {
        'password': 'kuma', 
        'permission': 'manager',
        'vacation_days': vacation_days},

    'Morris': {
        'password': 'morris', 
        'permission': 'staff',
        'vacation_days': vacation_days},
}

# 以字典方式紀錄不同功能的權限
filter_by_permission = {
    'highest_level': ['boss'],
    'medium_level': ['boss', 'manager'],
    'lowest_level': ['boss', 'manager', 'staff']
}