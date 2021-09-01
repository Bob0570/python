#vct using for windows GUI

import sys
import tkinter 
import struct
import threading
import json
from PIL import Image, ImageTk

sys.path.append("../")
from alipay.alipay import *
from vos.vos_draw import Vosdraw as Vosui
from vos.vos_misc import *

my_list=[
    {'type':'label', 	'pos_xy':[200,10], 	'size_wh':[100,50],     'text':'咖啡屋',   'command':None, 'object':None}, 
    {'type':'listbox',  'pos_xy':[50,70], 	'size_wh':[600,600],    'text':'list',     'command':None, 'object':None},
    {'type':'button', 	'pos_xy':[200,670], 'size_wh':[100,30],     'text':'付款',     'command':None, 'object':None},
]
allCafeList=[
    [20.01, 	'厚乳拿铁'], 
    [20.01, 	'冲绳黑糖拿铁'], 
    [20.01, 	'焦糖玛奇朵'], 
    [20.01, 	'标准美式'], 
    [20.01, 	'加浓美式'], 
    [20.01, 	'卡布奇洛'], 
    [20.01, 	'摩卡'], 
]

def sendWechatMsg(WechatMsg):
    url_token = 'https://api.weixin.qq.com/cgi-bin/token?'
    res = requests.get(url=url_token,params={
            "grant_type": 'client_credential',
            'appid':'wxe4f09c2cdde2975a',# 这里填写上面获取到的appID
            'secret':'f810ffb878a303485caf6e7618594e85',# 这里填写上面获取到的appsecret
            }).json()
    print(res)
    token = res.get('access_token')
    #print(res)

    url_msg ='https://api.weixin.qq.com/cgi-bin/message/custom/send?'
    body = {
            "touser": 'ontAx6Id0-AHa6IVa7bKZXn26l8c',#这里必须是关注公众号测试账号后的用户id
            "msgtype":"text",
            "text":{
            "content":WechatMsg
            }
        }

    res =requests.post(url=url_msg,params = {
            'access_token': token  #这里是我们上面获取到的token
        },data=json.dumps(body,ensure_ascii=False).encode('utf-8'))
    #print(res)   

def checkBillTask(billWindow, tradeSn, note_str, billList):
    billFlag = 0
    while True:
        vos_taskSleep(200)
        tradeResult = ckeck_ali_trade(tradeSn)
        if(tradeResult['trade_status'] == 'WAIT_BUYER_PAY'):
            if(billFlag == 0):
                noteStr = tradeResult['phone number'] + ' Paying...'
                note_str.set(noteStr)
                billFlag = 1
        elif(tradeResult['trade_status'] == 'TRADE_SUCCESS'):
            noteStr = tradeResult['phone number'] + ' Paying...Done!!!!'
            note_str.set(noteStr)
            WechatMsg = tradeResult['phone number'] + 'Pay ' + tradeResult['buyer_pay_amount'] + '\n' + billList
            sendWechatMsg(WechatMsg)
            vos_taskSleep(2000)
            billWindow.destroy()
            return

def checkBillButton(billWindow):
    billWindow.destroy()

def showBillWindow(billing, totalMoney,tradeSn):    
    billWindow=tkinter.Toplevel()
    billWindow.title=("扫码支付") 
    billWindow.geometry("500x700+10+10")

    imgFile = tradeSn + '.png'
    image = Image.open(imgFile) 
    img = ImageTk.PhotoImage(image)
    canvas1 = tkinter.Canvas(billWindow, width = image.width ,height = image.height, bg = 'white')
    canvas1.create_image(0,0,image = img,anchor="nw")
    canvas1.pack()  

    note_str = tkinter.StringVar()
    noteStr = '                请扫码支付--' + '总金额：' + str(totalMoney)
    note_str.set(noteStr)
    labelName = tkinter.Label(billWindow, textvariable=note_str, bg='black', fg='white', justify=tkinter.LEFT,anchor='center')
    labelName.place(x=image.width/8, y=image.height+10,width=400, height=30)

    billList = ''
    for billItem in billing:
        billList += billItem['name'] + ': ' + billItem['wendu'] + ' ' + billItem['sugar'] + '\n'
    labelName = tkinter.Label(billWindow, text=billList, justify=tkinter.LEFT,anchor='nw')
    labelName.place(x=image.width/8, y=image.height+40,width=300, height=100)

    buttonName = tkinter.Button(billWindow, text='Cancel', command=lambda:checkBillButton(billWindow))
    buttonName.place(x=image.width/2, y=image.height+220, width=80, height=20)

    checkBill = threading.Thread(target=checkBillTask, args=(billWindow, tradeSn, note_str, billList))
    checkBill.setDaemon(True)
    checkBill.start()

    billWindow.mainloop()

def mkCafeMenu(cafeList):
    i=0
    menu_list = []
    menu_name = {}
    menu_money = {}
    menu_wendu = {}
    menu_sugar = {}

    for cafe in allCafeList:
        menu_name[i] = {'type':'ckbutton', 	'pos_xy':[60,80], 	'size_wh':[150,30],     'text':'None',   'option':None, 'object':None, 'money':0.01}
        menu_name[i]['pos_xy'][1] += i*60
        menu_name[i]['money'] = allCafeList[i][0]
        menu_name[i]['text'] = allCafeList[i][1]
        menu_list.append(menu_name[i])

        menu_money[i] = {'type':'label', 	'pos_xy':[60,110], 	'size_wh':[150,30],     'text':'money:',      'command':None, 'object':None}
        menu_money[i]['pos_xy'][1] += i*60
        menu_money[i]['text'] = '      '+ str(allCafeList[i][0])
        menu_list.append(menu_money[i])

        menu_wendu[i] = {'type':'rdbutton', 	'pos_xy':[250,80], 	'size_wh':[80,20],   'text':['热饮','常温','加冰'],   'option':None, 'object':None, 'direct':'Horizen'}
        menu_wendu[i]['pos_xy'][1] += i*60
        menu_list.append(menu_wendu[i])

        menu_sugar[i] = {'type':'rdbutton', 	'pos_xy':[250,100], 	'size_wh':[80,20],   'text':['全糖','七分糖', '半糖','无糖'],   'option':None, 'object':None, 'direct':'Horizen'}
        menu_sugar[i]['pos_xy'][1] += i*60
        menu_list.append(menu_sugar[i])

        i += 1
    return menu_list

def mkCafebilling(menu_list):
    listCnt = len(menu_list)
    totalMony = 0
    billing = []
    for i in range(0,listCnt,4):
        menu_name = menu_list[i]
        menu_money = menu_list[i+1]
        menu_wendu = menu_list[i+2]
        menu_sugar = menu_list[i+3]
        if(menu_name['option'].get() == 1):
            items = {'name': menu_name['text'], 'money':menu_name['money'], 'wendu':menu_wendu['text'][menu_wendu['option'].get()], 'sugar':menu_sugar['text'][menu_sugar['option'].get()]}
            billing.append(items)
    return billing

def addAllCafe():
    cafeList = my_list[1]['object']
    for item in allCafeList:
        cafeList.insert('end', item['name'])

def payProc():
    billing = mkCafebilling(menuList)
    totalMoney = 0
    for billItem in billing:
        totalMoney += billItem['money']    
    
    if(totalMoney == 0):
        return

    timeStr = vos_getTimeStr()
    timeStr2 = timeStr.split(' ')
    tradeSn = timeStr2[1].replace(':','')
    mk_ali_qrcode(str(totalMoney), tradeSn)
    showBillWindow(billing, totalMoney,tradeSn)
    
root = tkinter.Tk()
root.title('cafe shopping')
root.geometry('700x710+10+10')
my_draw = Vosui(root)

my_list[2]['command']= payProc
my_draw.drawList(my_list)
menuList = mkCafeMenu(allCafeList)
my_draw.drawList(menuList)


root.mainloop()