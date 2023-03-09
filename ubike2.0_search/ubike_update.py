# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 17:35:06 2023

@author: user
"""

import pymysql
import pandas as pd
import time,sched
from datetime import datetime

url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
columns = 'mday、sno、sna、sarea、ar、lat、lng、tot、sbi、bemp、act、updateTime'.split('、')


#資料庫連線
dbsetting={
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'123456789',
    'db':'ubike',
    'charset':'utf8'
}


#匯入資料
def get_data(sec,end_date=None):
#先整理
    datas = pd.read_json(url)
    udata = datas[columns]
    #仍在運作的、不重複的
    udata = udata[udata['act']==1].drop_duplicates()

    n=0
    conn=pymysql.connect(**dbsetting)
    cursor=conn.cursor()

    #第一次匯入
    sql='select * from taipei'
    res = cursor.execute(sql)
    if res==0:
        for data in udata.values:
            sql=f'insert into taipei(mday,sno,sna,sarea,ar,lat,lng,tot,sbi,bemp,act,updateTime) values("{data[0]}","{data[1]}","{data[2]}","{data[3]}","{data[4]}","{data[5]}","{data[6]}",{data[7]},{data[8]},{data[9]},{data[10]},"{data[11]}")'
            cursor.execute(sql)

    #第二次匯入開始，篩選有更新的資料
    else:
        for data in udata.values:
            sql=f'select * from taipei where sno="{data[1]}" and mday="{data[0]}"'
            res=cursor.execute(sql)

            if res==0:
                n+=1
                sql=f'update taipei set mday="{data[0]}",sbi={data[8]},bemp={data[9]},updateTime="{data[11]}" where sno="{data[1]}"'
                cursor.execute(sql)
            else:
                pass

    conn.commit()
    conn.close()
    print(datetime.now())
    print(f'已更新{n}筆資料')
    
    if datetime.now() <= end_date:
        s.enter(sec,0,get_data,(sec,end_date))




end_date=datetime(2023,4,1,24,0,0)
sec=120

s=sched.scheduler(time.time,time.sleep)
s.enter(0,0,get_data,(sec,end_date))
s.run()









