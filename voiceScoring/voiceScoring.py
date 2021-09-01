import time
import threading
from voice2text import *
import tkinter.font as tkFont

voiceStatus = {'status':'waitting input'}  #['waitting input', 'listening', 'translating', 'done']

def scoreSpeakOut(scoreVal1, scoreVal2):
    outText = "红方蓝方比分" + str(scoreVal1) + "比" + str(scoreVal2)
    audioPlayFromText(outText)

def voiceInput():
    if(voiceStatus['status'] == 'waitting input'):
        voiceStatus['status'] = 'listening'

def voiceTextParser(voiceList):
    voiceText = voiceList[0]
    if("土豆加" in voiceText) or ("土豆胜" in voiceText):
        result = 11 #红方加分
    elif("土豆减" in voiceText) or ("土豆输" in voiceText):    
        result = 10 #红方减分
    elif("地瓜加" in voiceText) or ("地瓜胜" in voiceText):
        result = 21 #蓝方加分
    elif("地瓜减" in voiceText) or ("地瓜输" in voiceText):    
        result = 20 #蓝方减分        
    elif("比分清" in voiceText) or ("开始" in voiceText):    
        result = 3 #比分请0        
    elif("交换" in voiceText) or ("叫唤" in voiceText):    
        result = 4 #交换场地     
    else:
        result = 0  #do nothing

    return result

def voiceTask(root, score1, score2, info, name1, name2):
    scoreVal1 = 0
    scoreVal2 = 0
    val_sw = 0 #场地
    client = mkAiClient()
    
    while True:        
        if(voiceStatus['status'] == 'listening'):
            info.set("listening")
            audio_record('score.wav', 3)
            voiceStatus['status'] = 'translating'
        elif(voiceStatus['status'] == 'translating'):
            info.set("translating...")
            audioPlayFromText('语音识别中')
            #text = '红方加分红方胜'
            #time.sleep(1000/1000)
            text = audio2text(client, 'score.wav', 1537)
            #info.set("translating...done!")
            info.set(text)
            voiceStatus['status'] = 'done'

            reslt = voiceTextParser(text)
            if(reslt == 11): #红方加分
                scoreVal1 += 1
            elif(reslt == 10): #红方减分
                scoreVal1 -= 1    
            elif(reslt == 21): #蓝方加分
                scoreVal2 += 1
            elif(reslt == 20): #蓝方减分
                scoreVal2 -= 1            
            elif(reslt == 3): #比分请0
                scoreVal1 = 0
                scoreVal2 = 0
            elif(reslt == 4): #交换场地
                val_sw += 1
                val_sw = val_sw%2        
            else: #do nothing
                time.sleep(10/1000)

            if(val_sw == 0):
                name1.config(text='红军')
                name1.config(fg='red')
                name2.config(text='蓝军')
                name2.config(fg='blue')

                score1.config(text=str(scoreVal1))
                score1.config(fg='red')
                score2.config(text=str(scoreVal2))
                score2.config(fg='blue')
            else:
                name2.config(text='红军')
                name2.config(fg='red')
                name1.config(text='蓝军')
                name1.config(fg='blue')

                score2.config(text=str(scoreVal1))
                score2.config(fg='red')
                score1.config(text=str(scoreVal2))
                score1.config(fg='blue')

            scoreSpeakOut(scoreVal1, scoreVal2)

        elif(voiceStatus['status'] == 'done'):
            time.sleep(500/1000)
            #info.set("waitting input")
            voiceStatus['status'] = 'waitting input'
        else:
            time.sleep(100/1000)

root = tkinter.Tk()
root.title('audio Scoring')
root.geometry('620x300+200+200')
my_draw = Vosui(root)

font1 = tkFont.Font(size=40)

name1 = tkinter.Label(root, text='红军', fg='red', font=font1)
name1.place(x=150, y=50,width=120, height=60)
name2 = tkinter.Label(root, text='蓝军', fg='blue', font=font1)
name2.place(x=310, y=50,width=120, height=60)

score1 = tkinter.Label(root, text='0', bg='black', fg='red', font=font1)
score1.place(x=150, y=120,width=120, height=60)
score2 = tkinter.Label(root, text='0', bg='black', fg='blue', font=font1)
score2.place(x=310, y=120,width=120, height=60)

name3 = tkinter.Label(root, text=':', fg='black', font=font1)
name3.place(x=280, y=115,width=20, height=60)

#button
buttonName = tkinter.Button(root, text='语音输入', command=voiceInput)
buttonName.place(x=220, y=220,  width=120, height=40)

#debug info
info = tkinter.StringVar()
info.set(" ")
scoreLab1 = tkinter.Label(root, textvariable=info, anchor='w')
scoreLab1.place(x=20, y=270,width=300, height=20)

pVoiceTask = threading.Thread(target=voiceTask, args=(root, score1, score2, info, name1, name2))
pVoiceTask.setDaemon(True)
pVoiceTask.start()

audioPlayFromText('比赛开始')
root.mainloop()

