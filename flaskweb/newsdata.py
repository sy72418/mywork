# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 14:55:04 2022

@author: user
"""

import requests

from bs4 import BeautifulSoup

import db

from pymysql.converters import escape_string


#抓新聞
url = "https://www.starbucks.com.tw/about/newsroom/aboutpsc.jspx"

data = requests.get(url)
data.encoding = "utf8"

data = data.text

soup = BeautifulSoup(data,'html.parser')

data = soup.find('ul',class_='event')

ditem= data.find_all('a')

cursor = db.conn.cursor()

for d in ditem:
    title=d.find('h1').text
    content = d.find('h3').text
    
    title = escape_string(title)
    content = escape_string(content)
    
    sql = "select * from news where title='{}'".format(title)
    
    cursor.execute(sql)
    db.conn.commit()
    
    if cursor.rowcount == 0:
        sql = "insert into news(title,content) values('{}','{}')".format(title,content)
        
        cursor.execute(sql)
        db.conn.commit()

db.conn.close()





