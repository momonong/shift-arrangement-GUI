# 先以字典方式代替資料庫
personnel = {
    'Jonny': {
        'password': 'jonny', 
        'permission': 'boss',
        'vacation_days': 8},

    'KUMA': {
        'password': 'kuma', 
        'permission': 'manager',
        'vacation_days': 8},

    'Morris': {
        'password': 'morris', 
        'permission': 'staff',
        'vacation_days': 8},
}

# 以字典方式紀錄不同功能的權限
filter_by_permission = {
    'highest_level': ['boss'],
    'medium_level': ['boss', 'manager']
}