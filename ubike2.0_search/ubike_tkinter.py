# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 21:28:24 2023

@author: user
"""

import tkinter as tk
import pymysql

dbsetting={
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'123456789',
    'db':'ubike',
    'charset':'utf8'
}
conn = pymysql.connect(**dbsetting)

sql='select area from area'
cursor=conn.cursor()
cursor.execute(sql)
area=cursor.fetchall()

areas=['選擇地區']
for a in area:
    areas.append(a[0])
    

def show():
    global msg
    a = area.get()
    r = r1.get()
    win=tk.Toplevel(root)
    
    try:
        if a!='選擇地區' and r=="":
            sql='select sno,sna,sarea,ar,tot,sbi,bemp,updateTime from taipei where sarea="{}"'.format(a)
            
        elif a=='選擇地區' and r!="":
            sql = 'select sno,sna,sarea,ar,tot,sbi,bemp,updateTime from taipei where ar like "%{}%"'.format(r)
            cursor.execute(sql)
            msg=cursor.fetchall()
            
        elif a!='選擇地區' and r!="":
            sql='select sno,sna,sarea,ar,tot,sbi,bemp,updateTime from taipei where sarea="{}" and ar like "%{}%"'.format(a,r)
            cursor.execute(sql)
            msg=cursor.fetchall()
        
        else:
            msg="查無資訊！"
            return msg
            
        res=cursor.execute(sql)
        if res==0:
            msg="查無資訊！"
        else:
            msg=cursor.fetchall()

    
    except Exception as e:
        print(e)
    finally:
        
        win.title("ubike2.0資料")
        win.geometry("1300x700")
        bl=tk.Label(win,text='\n',padx=5,pady=5)
        bl.pack()
        
        canvas = tk.Canvas(win)
        canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        scrollbar = tk.Scrollbar(win, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.configure(yscrollcommand=scrollbar.set)

        
        fr=tk.Frame(canvas)
        canvas.create_window((0, 0), window=fr, anchor='nw')
        
        title=[]
        columns="站點代號、場站名稱、場站區域、地點、總停車格、目前車輛數、空位數、更新時間".split('、')
        for i in range(8):
            t=tk.StringVar()
            title.append(t)
            
            ta=tk.Label(fr,textvariable=title[i],font=(12,),padx=3,pady=3)
            title[i].set(columns[i])
            ta.grid(row=0,column=i,sticky='w')

        if msg!="查無資訊！":
            for i,data in enumerate(msg):
                d=[]
                for j in range(8):
                    t=tk.StringVar()
                    d.append(t)
                    
                    da=tk.Label(fr,textvariable=d[j],font=(12,),padx=3,pady=3)
                    d[j].set(data[j])
                    da.grid(row=i+1,column=j,sticky='w')
            
            fr.update_idletasks()
            canvas.config(scrollregion=canvas.bbox('all'))
            

                
        else:
            d=tk.Label(fr,text=msg,font=(14,),fg='red')
            d.grid(row=1,column=0,columnspan=8,sticky='nsew')
        
            fr.update_idletasks()
            canvas.config(scrollregion=canvas.bbox('all'))
            
        win.wait_window()

# 建立 Tkinter 的主視窗
root = tk.Tk()
root.geometry("600x200")
root.title('ubike2.0 查詢系統')

s1=tk.Label(root,text='台北市地區：',pady=5,font=(12,))
s1.place(x=15,y=15)


area = tk.StringVar()
# 設定預設選項
area.set(areas[0])
# 建立下拉式選單 widget
option_menu = tk.OptionMenu(root, area, *areas)
option_menu.config(width=8,bg='white')
# 將下拉式選單放置在視窗中
option_menu.place(x=115,y=15)

road=tk.Label(root,text='路口查詢：',pady=5,font=(12,))
road.place(x=230,y=15)

r1=tk.StringVar()
road1=tk.Entry(root,font=(12,),textvariable=r1,width=20)
road1.place(x=320,y=20)

sb=tk.Button(root,text='查詢',fg='blue',font=(9,),width=8,padx=5,pady=2,command=show)
sb.place(x=501,y=12)

root.mainloop()



    

