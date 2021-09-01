import os
import openpyxl

FileName_wordingTools = "PROXI_ListReport Wording Tools.xlsx"
Config_saveMultiFile = 0
Config_sheet = "Config"


config_input = {"String ID Col":'D6', "Start Row":'D7', "EndRow":'D8', "SheetName":'D9', "Lang Range":'F6', "English Idx":'F9'}
config_output = {"OutPutFilePath":'N5', "OutPutResultFileName":'N6', "OutPutErrorLogFileName":'N7', "OutPutSheetName":'N8', "OutPutType":'N9', "OutPutStrIDHeadFileName":'N10'}


config_result = {"Start Row":None, "EndRow":None, "SheetName":None, "String ID Col":None, "OutPutFilePath":None, "OutPutResultFileName":None, "OutPutStrIDHeadFileName":None}
config_rst_list = [] #[{"Lang Name":None, "Wording Col":None, "Hex flag":None}]

def mk_cfg_result():
    sht_cfg = wb_wdTls[Config_sheet]
    #make config_result
    config_result["Start Row"] = sht_cfg[config_input["Start Row"]].value
    config_result["EndRow"] = sht_cfg[config_input["EndRow"]].value
    config_result["SheetName"] = sht_cfg[config_input["SheetName"]].value
    config_result["String ID Col"] = sht_cfg[config_input["String ID Col"]].value
    config_result["OutPutResultFileName"] = sht_cfg[config_output["OutPutResultFileName"]].value
    config_result["OutPutStrIDHeadFileName"] = sht_cfg[config_output["OutPutStrIDHeadFileName"]].value
    config_result["OutPutFilePath"] = sht_cfg[config_output["OutPutFilePath"]].value

    #make config_rst_list
    Lang_Range = sht_cfg[config_input["Lang Range"]].value
    start_row, end_row = Lang_Range.split(':')
    end_row = end_row.replace('H', 'K')
    Lang_Range = start_row + ":"+ end_row
    for aa in sht_cfg[Lang_Range]:
        temp = {"Lang Name":aa[0].value, "Wording Col":aa[1].value, "Hex flag":aa[3].value}
        config_rst_list.append(temp)

def mk_wording_ID():
    #make Id_range
    Start_Row = config_result["Start Row"]
    EndRow = config_result["EndRow"]
    Id_Col = config_result["String ID Col"]
    Id_range = Id_Col + str(Start_Row) + ':' + Id_Col + str(EndRow)

    #make IDHeadFile
    sht_wording = wb_wdTls[config_result["SheetName"]]
    fd_IDHeadFile = open(config_result["OutPutFilePath"]+config_result["OutPutStrIDHeadFileName"], 'w')
    for aa in sht_wording[Id_range]:
        newWording = '\t' + aa[0].value + ',\r\n'
        fd_IDHeadFile.writelines(newWording)
    fd_IDHeadFile.close()   

def mk_wording_item(wording_item):
    if(Config_saveMultiFile == 1):
        #create result lang name
        result_name = config_result["OutPutFilePath"]+wording_item["Lang Name"] + '.inc'
        fd_ResultFile = open(result_name, 'w')
    
    #make wording_range
    Wording_Col = wording_item["Wording Col"]
    Start_Row = config_result["Start Row"]
    EndRow = config_result["EndRow"]
    wording_range = Wording_Col + str(Start_Row) + ':' + Wording_Col + str(EndRow)

    #make header
    header_str = '//' + wording_item["Lang Name"] + '\r\n'
    if(Config_saveMultiFile == 1):
        fd_ResultFile.writelines(header_str)
    else:    
        fd_ResultFileAll.writelines(header_str)
    header_str = '{' + '\r\n'
    if(Config_saveMultiFile == 1):
        fd_ResultFile.writelines(header_str)
    else:    
        fd_ResultFileAll.writelines(header_str)

    #make newWording
    sht_wording = wb_wdTls[config_result["SheetName"]]
    for aa in sht_wording[wording_range]:
        id_row = aa[0].row
        id_cell = config_result["String ID Col"] + str(id_row)
        header_id = sht_wording[id_cell].value
        header_wording = "\t/*" + '%-60s'%header_id + "*/"

        newWording = header_wording + '\t_S("'
        wordings = str(aa[0].value)
        if(wording_item["Hex flag"] == 1):
            for wd_chr in wordings:
                bb = '%x'%ord(str(wd_chr))  #convert to unicode
                #newWording += '\\x' + bb[2:4] + '\\x' + bb[0:2]
                newWording += '\\x' + bb.upper()
        else:
            newWording += wordings
        newWording += '"),\t\t\r\n'
        if(Config_saveMultiFile == 1):
            fd_ResultFile.writelines(newWording)
        else:    
            fd_ResultFileAll.writelines(newWording)

    #make tail
    tail_str = '},' + '\r\n\r\n'
    if(Config_saveMultiFile == 1):
        fd_ResultFile.writelines(tail_str)
        fd_ResultFile.close()
    else:    
        fd_ResultFileAll.writelines(tail_str)

    
wb_wdTls = openpyxl.load_workbook(FileName_wordingTools, data_only=True)
mk_cfg_result()
os.system("mkdir "+config_result["OutPutFilePath"])

#make IDHeatFile
mk_wording_ID()

#make ResultFile
if(Config_saveMultiFile != 1):
    fd_ResultFileAll = open(config_result["OutPutFilePath"]+config_result["OutPutResultFileName"], 'w')

for result in config_rst_list:
    mk_wording_item(result)    

if(Config_saveMultiFile != 1):
    fd_ResultFileAll.close()




