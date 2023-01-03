from django.shortcuts import render,redirect

# Create your views here.

from django.http import HttpResponseRedirect
from django.utils.html import format_html

from cart import models
from product.models import goods
from member.models import Member

import os
basedir = os.path.dirname(__file__)#抓取預設目錄
file = os.path.join(basedir,'ecpay_payment_sdk.py')

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    file
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime




cartlist = list() #購物車內容
customname = ''
customphone = ''
customaddress = ''
customemail = ''

ordertotal = ''
goodstitle = list() #購物車內的商品名稱

#增減購物車
def addtocart(request,ctype=None,productid=None):
    global cartlist
    
    if ctype=='add':
        product = goods.objects.get(id = productid)
        flag = True #預設購物車沒有相同商品
        
        #檢查購物車是否有此商品，重複就數量加一
        for unit in cartlist:
            if product.title == unit[0]:
                #數量加一
                unit[2]=str(int(unit[2])+1)
                #累計金額
                unit[3]=str(int(unit[3])+product.price)
                flag = False
                break
            
        #購物車沒有相同商品
        if flag:
            templist = list()
            templist.append(product.title)
            templist.append(str(product.price))
            templist.append('1')
            templist.append(str(product.price))
            cartlist.append(templist)
            
        request.session['cartlist'] = cartlist
        
        return redirect('/product/')
    
    #更新購物車
    elif ctype =='update':
        n=0
        for unit in cartlist:
            amount = request.POST.get('qty'+str(n))
            if len(amount) == 0:
                amount='1'
            elif int(amount) <=0:
                amount = '1'
            else:
            
                unit[2] = amount
                unit[3] = str(int(unit[1])*int(unit[2]))
            n+=1
        
        request.session['cartlist'] = cartlist
        
        return redirect('/cart/')
    
    #清空購物車
    elif ctype =='empty':
        cartlist = list()
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
    
    #刪除商品
    elif ctype == 'remove':
        del cartlist[int(productid)]
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
        


#顯示購物車
def cart(request):
    global cartlist
    allcart = cartlist
    total = 0
    for unit in cartlist:
        total += int(unit[3])
    
    if total>0 and total<500:
        shipping = 60
    else:
        shipping = 0
    grandtotal = total+shipping
    
    return render(request,'cart.html',locals())
    



#結帳頁面
def cartorder(request):
    #要先登入，才能結帳
    if "mymail" in request.session and "isalive" in request.session:
        global cartlist,customemail
        allcart = cartlist
        total = 0
        for unit in cartlist:
            total += int(unit[3])
        
        if total>0 and total<500:
            shipping = 60
        else:
            shipping = 0
        grandtotal = total+shipping
        
        email = request.session['mymail']
        custom = Member.objects.get(email=email)
        name = custom.name
        phone = custom.phone
        address = custom.address
        
        return render(request,'cartorder.html',locals())
    
    else:
        return HttpResponseRedirect('/login')
        
        



#確認資料並送出，將訂單寫到資料庫
#更新會員資料
def cartok(request):
    global cartlist,customname,customphone,customaddress,customemail
    
    global ordertotal, goodstitle
    
    total = 0
    for unit in cartlist:
        total += int(unit[3])
    
    if total>0 and total<500:
        shipping = 60
    elif total==0:
        return HttpResponseRedirect('/product')
    else:
        shipping = 0
    grandtotal = total+shipping
    
    ordertotal = grandtotal
    customname = request.POST.get('cuname','')
    customphone = request.POST.get('cuphone','')
    customaddress = request.POST.get('cuaddr','')
    customemail = request.POST.get('cuemail','')
    paytype = request.POST.get('paytype','')
    
    #新增訂單到資料表中
    unitorder = models.Ordersmodel.objects.create(subtotal=total, shipping=shipping, grandtotal=grandtotal, customname = customname, customemail=customemail, customphone=customphone, customaddress=customaddress, paytype=paytype)
    
    #將商品新增到明細表中
    for unit in cartlist:
        goodstitle.append(unit[0])
        total = int(unit[1])*int(unit[2])
        unitdetail = models.Detailmodel.objects.create(dorder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2],dtotal=total)
        
    orderid = unitorder.id
    grandtotal = unitorder.grandtotal
    name = unitorder.customname
    email = unitorder.customemail
    phone = unitorder.customphone
    address = unitorder.customaddress
    
    detail = models.Detailmodel.objects.filter(dorder_id=orderid)
    cartlist = list()
    request.session['cartlist'] = cartlist
    
    
    #更新會員資料
    addinfo = request.POST.get('info')
    
    if addinfo != None:
        addphone = request.POST.get('cuphone','')
        addaddress = request.POST.get('cuaddr','')
        customemail = request.POST.get('cuemail','')
        info = Member.objects.filter(email=customemail).update(phone=addphone,address=addaddress)

    
    if paytype == "信用卡":
        
        return HttpResponseRedirect('/creditcard',locals())
    elif paytype == "ATM轉帳":
        return HttpResponseRedirect('/atm',locals())
    else:
        return render(request,'cartok.html',locals())




#顯示會員所有訂單
def myorder(request):
    if "mymail" in request.session and "isalive" in request.session:
        
        email = request.session['mymail']
        
        order = models.Ordersmodel.objects.filter(customemail=email).order_by('-id')
        for unit in order:
            detail= models.Detailmodel.objects.filter(dorder_id=unit.id)
        
        return render(request,'orderlist.html',locals())
    
    else:
        return HttpResponseRedirect('/login')


def Ecpaycredit(request):
    
    global goodstitle,ordertotal
    title = ""
    for i in goodstitle:
        title+=i+"*"
        
        
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': ordertotal,
        'TradeDesc': 'Bookstore-訂單',
        'ItemName': title,
        'ReturnURL': 'https://www.lccnet.com.tw/lccnet',
        'ChoosePayment': 'Credit',
        'ClientBackURL': 'https://www.lccnet.com.tw/lccnet',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://www.lccnet.com.tw/lccnet',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }
    
    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }
    
    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }
    
    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }
    
    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )
    
    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)
    
    # 合併發票參數
    order_params.update(inv_params)
    
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
    
        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        
        html = format_html(html) #格式化
        return render(request,'paycredit.html',locals())
    except Exception as error:
        print('An exception happened: ' + str(error))


def atm(request):
    
    global goodstitle,ordertotal
    title = ""
    for i in goodstitle:
        title+=i+"*"
    
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': ordertotal,
        'TradeDesc': 'Bookstore-訂單',
        'ItemName': title,
        'ReturnURL': 'https://www.lccnet.com.tw/lccnet',
        'ChoosePayment': 'ATM',
        'ClientBackURL': 'https://www.lccnet.com.tw/lccnet',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://www.lccnet.com.tw/lccnet',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }
    
    extend_params_1 = {
        'ExpireDate': 7,
        'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
        'ClientRedirectURL': '',
    }
    
    
    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }
    
    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )
    
    # 合併延伸參數
    order_params.update(extend_params_1)
    
    # 合併發票參數
    order_params.update(inv_params)
    
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
    
        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        html = format_html(html) #格式化
        return render(request,'atm.html',locals())
    
    except Exception as error:
        print('An exception happened: ' + str(error))
    