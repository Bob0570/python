from PIL import Image
import pytesseract

#安装Tesseract-OCR，使用tesseract.exe
#配置： C:\python\Lib\site-packages\pytesseract\pytesseract.py中， tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'
#各版本语言包下载路径：https://github.com/tesseract-ocr/tesseract/wiki/Data-Files


img = Image.open('pic1.png')

text=pytesseract.image_to_string(img)
#text=pytesseract.image_to_string(img,lang='chi_sim')
print(text)