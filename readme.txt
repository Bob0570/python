https://www.python.org/
libs: 	https://www.lfd.uci.edu/~gohlke/pythonlibs/#bsdiff4
intall:        pip install path\*.whl

1--vct工具: 
   dvct.py: Dos命令行界面
   wvct.py:Windows图像界面

2--Wording生成工具：mk_wording.py
   使用方法：将mk_wording.py中FileName_wordingTools = "ZOLOX ListReport Wording Tools.xlsx"改成指定的excel文件
  
3--code size统计工具：cs_statics.py
   使用方法：source_file = "mfp.axf"或者source_file = "simva.out.elf"

4--http：
   3rdParty_app1.py: client工具， 使用方法：有help帮助命令，先建立连接，输入connect X.X.X.X, http包内容从http_app.xlsx里获取
   3rdParty_ser2.py/3rdParty_app2.py：server工具, 不使用http库，可以灵活解析和构造http报文
   	使用方法：有help帮助命令，先建立连接，输入connect X.X.X.X, http包内容从http_app2.xlsx里获取
   http_serClient.py: 既是server也是client，输入serip X.X.X.X指定对方server IP地址

5--3rd Party tool：3pt.py

6--支付宝二维码付款：alipay.py
   使用方法：命令行界面，输入钱数和名字，当前目录产生付款二维码png图像文件

7--咖啡屋：cafeShop.py
   使用方法：图形界面，选择咖啡种类，点击付款，刷码支付，微信通知店主咖啡数量总类和买主手机号
   
8--语音输入识别：voice2text.py
   使用方法：图形界面，选择语音种类（支持普通话/四川话/广东话/英语），点击开始说话，
             对准麦克风说话，然后翻译成中文或英文，显示识别的文字，并用普通话或英文播报文字

9--语音计分器：voiceScoring.py
   使用方法：图形界面，只支持普通话输入，关键词汇见函数：voiceTextParser内容
             由于使用的是百度AI短语音在线识别，速度很慢，所以不支持实时语音采集，每次语音输入前需点击语音输入按钮，

10--图片取词：getTextFromPic.py
    借助工具Tesseract-OCR实现识别图片中的字符

11--log筛选：VerifyLogImp.py (支持多个log files)
    使用方法：图形界面
    
12--图像识别：Margin_Adjust.py
    利用Opencv 图像识别自动计算Scan Margin 偏移值和缩放比例值，辅助Scan Margin SP value 设置  

13--函数超大局部变量统计工具：code_stack/check_stack.py
   使用方法：source_file = "mfp.axf"，生成excel文件
    
    
    