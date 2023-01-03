# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 19:49:12 2022

@author: user
"""

import requests

from bs4 import BeautifulSoup

import re

import db

from pymysql.converters import escape_string



#drinktype
url = "https://www.starbucks.com.tw/products/drinks.jspx"

data = requests.get(url)

data.encoding = "utf8"

data = data.text

soup = BeautifulSoup(data,'html.parser')

data = soup.find('ul',class_= 'menuof line4')

ditem = data.find_all('a')

cursor = db.conn.cursor()

for row in ditem:
    name = row.find('h1').text
    info = row.find('h3').text
    
    sql = "select * from drinktype where name='{}'".format(name)
    
    cursor.execute(sql)
    db.conn.commit()
    
    if cursor.rowcount == 0:
        sql = "insert into drinktype(name,info) values('{}','{}')".format(name,info)
        
        cursor.execute(sql)
        db.conn.commit()    
    
    
def getdata(url,typeid):
    data = requests.get(url)

    data.encoding = "utf8"

    data = data.text

    soup = BeautifulSoup(data,'html.parser')  
    
    data = soup.find('div',class_='content')

    data= data.find_all('article')
    
    for x in data:
        nd = x.find_all('li')
        for y in nd:
            name= y.find('h1').text
            ename = y.find('h3').text
            ename = escape_string(ename)
            
            a = y.find('img').get('src')
            p = r'product/(.+)'
            m = re.search(p,a)
            
            
            sql = "select * from drink where chname='{}'".format(name)
            
            cursor.execute(sql)
            db.conn.commit()
            
            if cursor.rowcount == 0:
                sql = "insert into drink(chname,enname,photo,typeid) values('{}','{}','{}','{}')".format(name,ename,m.group(1),typeid)
                
                cursor.execute(sql)
                db.conn.commit()
                   

#咖啡飲品   
url = "https://www.starbucks.com.tw/products/drinks/view.jspx?catId=1"
getdata(url,1)

#茶那堤
url = "https://www.starbucks.com.tw/products/drinks/view.jspx?catId=8"
getdata(url,2)

#星冰樂
url = "https://www.starbucks.com.tw/products/drinks/view.jspx?catId=4"
getdata(url,3)

#冷萃咖啡
url="https://www.starbucks.com.tw/products/drinks/view.jspx?catId=40"
getdata(url,4)

#其他飲料
url = "https://www.starbucks.com.tw/products/drinks/view.jspx?catId=10"
getdata(url,6)

#罐裝飲料
url="https://www.starbucks.com.tw/products/drinks/view.jspx?catId=26"
getdata(url,5)

db.conn.close()

      


