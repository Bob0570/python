#code size statics for simva.out.elf
import os
import openpyxl

#source_file = "simva.out.elf"
source_file = "source\\mfp_v014.axf"
temp_file = "source\\codeSize.map"
conv_command = "C:\\CodeSourcery\\SourceryLite\\bin\\arm-none-eabi-nm.exe -S -l " + source_file + " > " + temp_file
Statics_sheet = "statics"
Statics_result_file = "codeSizeStatics.xlsx"

ModuleDict = {"BSP":'BSP', "DPS":'DPS', "DENS":'net', "DENS_M":'net', "EMUL":'EMUL', "FAX":'FAX', "FAXCORE":'FAXCORE', "MPRINT":'MPRINT',"SYS":'SYS',  \
    "inferno":'inferno', "ipssky":'ipssky', "VOS":'VOS'}

ModuleSize = {"BSP":0, "DPS":0, "DENS":0, "DENS_M":0, "EMUL":0, "FAX":0, "FAXCORE":0, "MPRINT":0,"SYS":0,  \
    "inferno":0, "ipssky":0, "VOS":0, "other":0, "noName":0}

def mk_lineList(lineList):
    #for so lib
    if(lineList[0] == 'U'): #.so
        if '@@' in lineList[1]:
            name, soLib = lineList[1].split('@@')
        elif '@' in lineList[1]:
            name, soLib = lineList[1].split('@')
        else:
            name, soLib = lineList[1], 'NONE'
        lineList[0] = 'so'
        lineList[1] = 'so'
        lineList.append('text')
        lineList.append(name)
        lineList.append(soLib)
        return 0
    
    #for no name
    cnt_lineList = len(lineList)
    if(cnt_lineList < 4):
        return 1

    #Type
    if((lineList[2] == 't') or (lineList[2] == 'T')): 
        lineList[2] = 'text'
    elif((lineList[2] == 'b') or (lineList[2] == 'B')):
        lineList[2] = 'bss'
    elif((lineList[2] == 'd') or (lineList[2] == 'D')):    
        lineList[2] = 'data'
    elif((lineList[2] == 'r') or (lineList[2] == 'R')):    
        lineList[2] = 'rdata'
    else:
        return 1

    #size
    bb = int(lineList[1], 16)
    lineList[1] = bb

    #remove unvalid symbl name:
    if "__func__" in lineList[3]:
        return 1
    if "__FUNCTION__" in lineList[3]:
        return 1

    #no fileName
    if(cnt_lineList == 4):
        ModuleSize['noName'] += bb
        
        #Address(DEC)
        lineList.append('')
        lineList.append('')
        lineList.append('')
        bb = int(lineList[0], 16)
        lineList[6] = bb
        return 0
    
    #Module
    whole_fileName = lineList[4]
    lineList[4] = 'other'
    for keys in ModuleDict.keys():
        if keys in whole_fileName:
            lineList[4] = ModuleDict[keys]
            ModuleSize[keys] += bb
            break
    if(lineList[4] == 'other'):
        ModuleSize['other'] += bb
        
    #FileName
    filePathList = whole_fileName.split('/')
    cnt = len(filePathList)
    fileName = filePathList[cnt-1]
    fileName2, lines = fileName.split(':')
    lineList.append(fileName2)
    
    #Address(DEC)
    lineList.append(0)
    bb = int(lineList[0], 16)
    lineList[6] = bb
    
    return 0


print(conv_command+'...')
os.system(conv_command)
print('done!\r\n')

wb = openpyxl.Workbook()
ws = wb.active
ws.title = Statics_sheet
ws.append(["Address(HEX)", "Size", "Type", "Name", "Module", "FileName", "Address(DEC)"])

line_cnt = 0
fd_temp = open(temp_file, 'r')
for line in fd_temp.readlines():
    line_ls = line.split()
    if(mk_lineList(line_ls) == 0):
        ws.append(line_ls)
        line_cnt += 1

print("line_cnt=", line_cnt)
fd_temp.close()

ws.append([" ", " ", " ", " ", " ", " "])
ws.append(list(ModuleSize.keys()))
ws.append(list(ModuleSize.values()))

ws.auto_filter.ref = 'A:G'
ws.auto_filter.add_sort_condition('G:G')

wb.save(Statics_result_file)







