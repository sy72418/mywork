# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 11:50:18 2022

@author: user
"""

import requests

from bs4 import BeautifulSoup

import db

from pymysql.converters import escape_string



cursor = db.conn.cursor()
def get_soup(url,post_data=None,get_data=None):
    user_agent={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    try:
        if post_data is not None :
            resp = requests.post(url,post_data,headers=user_agent)
        elif get_data is not None :
            resp = requests.get(url,get_data,headers=user_agent)
        else:
            resp = requests.get(url,headers=user_agent)
        
        resp.encoding='utf-8'
        if resp.status_code==200:
            soup=BeautifulSoup(resp.text,'lxml')
            return soup
    except Exception as e:
        print(e)
    print(resp.status_code)
    return None

def get_data(url,typeid):
    soup = get_soup(url)
    f = 'https://www.starbucks.com.tw'
    t = soup.find_all('article')
    
    for i in t:
        infos = i.find_all('a')
        for info in infos:
            title = info.find('h1').text.strip()
            ename = info.find('h3').text.strip()
            ename = escape_string(ename)
            photo_url = f+info.find('img').get('src')
            link_url = f+info.get('href')
            
            sql = "select * from drinks where chname='{}'".format(title)
            cursor.execute(sql)
            db.conn.commit()
            
            if cursor.rowcount == 0:
                sql = "insert into drinks(chname,ename,photo_url,link_url,typeid) values('{}','{}','{}','{}','{}')".format(title,ename,photo_url,link_url,typeid)
                cursor.execute(sql)
                db.conn.commit()
        
#url = 'https://www.starbucks.com.tw/products/drinks/view.jspx?catId=1' 
#get_data(url,1)


url = 'https://www.starbucks.com.tw/products/drinks/view.jspx?catId=8'
get_data(url,2)

url='https://www.starbucks.com.tw/products/drinks/view.jspx?catId=4'
get_data(url,3)

url='https://www.starbucks.com.tw/products/drinks/view.jspx?catId=40'
get_data(url,4)

url='https://www.starbucks.com.tw/products/drinks/view.jspx?catId=26'
get_data(url,5)

url='https://www.starbucks.com.tw/products/drinks/view.jspx?catId=10'
get_data(url,6)