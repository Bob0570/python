''' 使用windows系统语音识别
import speech

while True:
    say = speech.input()
    print(say)
    speech.say("you say:"+say)
'''

import sys
import tkinter 
import pyaudio #pip install *.whl
import wave
from tqdm import tqdm
from aip import AipSpeech #pip install baidu-aip
import win32com.client as win  #pip install pywin32
sys.path.append("../")
from vos.vos_draw import Vosdraw as Vosui

# 用Pyaudio库录制音频
#   out_file:输出音频文件名
#   rec_time:音频录制时间(秒)
def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #16bit编码格式
    CHANNELS = 1 #1 #单声道
    RATE = 16000 #44100 #16000采样频率    

    p = pyaudio.PyAudio()

    # 创建音频流 
    stream = p.open(format=FORMAT, # 音频流wav格式
                    channels=CHANNELS, # 单声道
                    rate=RATE, # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK) 

    #print("Start Recording...") 
    frames = [] # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)    

    # 录制完成
    stream.stop_stream()
    stream.close()
    p.terminate()
    #print("Recording Done...") 

    # 保存音频文件
    wf = wave.open(out_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio_callback(wave_path):
    CHUNK = 1024
    wf = wave.open(wave_path, 'rb')
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)
    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)
    # read data
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)
    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()

def audioPlayFromText(text):
    speak = win.Dispatch("SAPI.SpVoice")
    #speak.Speak("红方蓝方比分是3比2")
    speak.Speak(text)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 读取paudio录制好的音频文件, 调用百度语音API, 设置api参数, 完成语音识别
#    client:AipSpeech对象
#    afile:音频文件
#    voiceType: 语言类型(见下表), 默认1537(普通话 输入法模型)
def audio2text(client, afile, voiceType):
    fp = open(afile, 'rb')
    audioContent = fp.read()

    # cuid    String  用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内
    result = client.asr(audioContent, 'wav', 16000, {"cuid": 'B8-CA-3A-B6-D0-96', "dev_pid": voiceType,})

    # 如果err_msg字段为"success."表示识别成功, 直接从result字段中提取识别结果, 否则表示识别失败
    if result["err_msg"] == "success.": 
        return result["result"]
    else:
        return ""

def inputProc():
    voiceList = {'普通话':1537, '四川话':1837, '广东话':1637, '英语   ':1737, '普通话远场':1936}
    option = pt_list[3]['option'].get()
    voice = pt_list[3]['text'][option]
    voiceType = voiceList[voice]
    
    audio_record('voice.wav', 4)

    note_str = tkinter.StringVar()
    note_str.set("语音识别中......")
    labelName = tkinter.Label(root, textvariable=note_str, bg='black', fg='white', justify=tkinter.LEFT, anchor='w')
    labelName.place(x=52, y=60,width=380, height=60)

    text = audio2text(client, 'voice.wav', voiceType)
    print(text)
    note_str.set(text)
    audioPlayFromText(text)
    #play_audio_callback('voice.wav')
    
def mkAiClient():
    APP_ID = '23672653'
    API_KEY = 'et1xX06PhOjeokuUoPQSjV3Y'
    SECRET_KEY = 'mA2DsAAaqdIrxzGDB1hHoWLnCKpcb7bi'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)    
    return client

if __name__ == "__main__":
    pt_list=[
        {'type':'label', 	'pos_xy':[480,60], 	'size_wh':[100,40],     'text':'选择语言',   'command':None, 'object':None}, 
        {'type':'listbox',  'pos_xy':[50,50], 	'size_wh':[400,200],    'text':'list',     'command':None, 'object':None},
        {'type':'button', 	'pos_xy':[200,270], 'size_wh':[100,30],     'text':'开始说话',     'command':None, 'object':None},
        {'type':'rdbutton', 'pos_xy':[480,110], 'size_wh':[80,30],      'text':['普通话','四川话', '广东话','英语   '],   'option':None, 'object':None, 'direct':'Vertical'}
    ]

    client = mkAiClient()

    root = tkinter.Tk()
    root.title('voice to text')
    root.geometry('600x320+200+200')
    my_draw = Vosui(root)

    pt_list[2]['command']= inputProc
    my_draw.drawList(pt_list)

    root.mainloop()

