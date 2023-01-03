# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 20:56:10 2022

@author: user
"""

from flask import Flask,render_template,request,url_for,redirect

from flask_paginate import Pagination,get_page_parameter

import db


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/product',methods=['GET'])
def drink():
    item = request.args.get('click')
    page = request.args.get('page')
    
    
    if page == None:
        page=1
    
        if item == None:
            sql="select photo_url,link_url,chname,ename from drinks limit 15"
            sql1 = "select name from drinktype where id='{}'".format(item)
            sqlp = "select count(*) as allcount from drinks"
        
        else:
            sql1 = "select name from drinktype where id='{}'".format(item)
            sql = "select photo_url,link_url,chname,ename from drinks where typeid='{}' limit 15".format(item)
            sqlp = "select count(*) as allcount from drinks where typeid='{}'".format(item)
            
        cursor = db.conn.cursor()
        cursor.execute(sql1)
        db.conn.commit()
        typename = cursor.fetchone()
            
        
        cursor.execute(sql)
        db.conn.commit()
        res = cursor.fetchall()
        
        cursor.execute(sqlp)
        db.conn.commit()
        resp = cursor.fetchone()
        count = int(resp[0])
        
        pagination = Pagination(page=page,total=count,per_page=15)
    
        return render_template("product.html",tname=typename,result=res,pagination=pagination)
    
    else:
        #使用者按分頁
        page = request.args.get(get_page_parameter(),type=int,default=int(page))
        startPage= page-1
        
        if item == None:
            sql="select photo_url,link_url,chname,ename from drinks limit {},{}".format(startPage*15,15)
            sql1 = "select name from drinktype where id='{}'".format(item)
            sqlp = "select count(*) as allcount from drinks"
        
        else:
            sql1 = "select name from drinktype where id='{}'".format(item)
            sql = "select photo_url,link_url,chname,ename from drinks where typeid='{}' limit {},{}".format(item,startPage*15,15)
            sqlp = "select count(*) as allcount from drinks where typeid='{}'".format(item)
            
        cursor = db.conn.cursor()
        cursor.execute(sql1)
        db.conn.commit()
        typename = cursor.fetchone()
            
        
        cursor.execute(sql)
        db.conn.commit()
        res = cursor.fetchall()
        
        cursor.execute(sqlp)
        db.conn.commit()
        resp = cursor.fetchone()
        count = int(resp[0])
        
        pagination = Pagination(page=page,total=count,per_page=15)
        
        return render_template("product.html",tname=typename,result=res,pagination=pagination)
        

@app.route('/news')
def news():
    sql = "select title,content from news"
    
    cursor = db.conn.cursor()
    cursor.execute(sql)
    db.conn.commit()
    res = cursor.fetchall()
    
    return render_template("news.html",result=res)



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/addmessage',methods=['POST'])
def addcontact():
    if request.method == 'POST':
        username=request.form.get('username')
        email= request.form.get('email')
        subject=request.form.get('subject')
        content=request.form.get('content')
        
        sql = "insert into message(username,email,subject,content) values('{}','{}','{}','{}')".format(username,email,subject,content)
        
        cursor = db.conn.cursor()
        cursor.execute(sql)
        db.conn.commit()
        
    return redirect(url_for('contact'))
        
        
        
        
        
        



app.run(debug=True,host='0.0.0.0',port=5555)