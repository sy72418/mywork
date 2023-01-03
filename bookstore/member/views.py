from django.shortcuts import render

# Create your views here.

import hashlib
from .models import Member
from django.http import HttpResponseRedirect, HttpResponse


def login(request):
    
    msg = ""
    if "email" in request.POST:
        email = request.POST['email']
        password = request.POST['pwd']
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
        
        obj = Member.objects.filter(email=email,password=password).count()
        
        #檢查帳密
        if obj > 0:
            request.session['mymail'] = email
            request.session['isalive'] = True
            
            response = HttpResponseRedirect('/product')
            
            response.set_cookie('umail',email,max_age=1200)
            
            return response
        
        else:
            msg="帳號密碼有誤，請重新輸入"
            return render(request,'login.html',locals())
    
    else:
        #開分頁，還未登出時
        if 'mymail' in request.session and "isalive" in request.session:
            return HttpResponseRedirect('/product')
        #cookies有暫存資料，但已登出
        else:
            myemail = request.COOKIES.get('umail','')
            return render(request,'login.html',locals())


def logout(request):
    del request.session['isalive']
    del request.session['mymail']
    
    response = HttpResponseRedirect('/login')
    response.delete_cookie('umail')
    
    return response



def register(request):
    
    msg=""
    if 'username' in request.POST:
        username = request.POST['username']
        sex = request.POST['sex']
        birthday = request.POST['birthday']
        email = request.POST['email']
        password = request.POST['pwd']
        
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
        
        obj = Member.objects.filter(email=email).count()
        if obj == 0:
            Member.objects.create(name=username,sex=sex,birthday=birthday,email=email,password=password)
            msg="已完成註冊！!"
        else:
            msg="此email已註冊過！！"
    
    return render(request,'register.html',locals())