#check function stack size
import os
import openpyxl

source_file = "mfp.axf"
temp_file = "mfp.s"
conv_command = "C:\\CodeSourcery\\SourceryLite\\bin\\arm-none-eabi-objdump.exe -d " + source_file + " > " + temp_file
Statics_sheet = "statics"
Statics_result_file = "funcStackSize.xlsx"

print(conv_command+'...')
os.system(conv_command)
print('done!\r\n')
wb = openpyxl.Workbook()
ws = wb.active
ws.title = Statics_sheet
ws.append(["FuncName", "stackSize"])

fd_temp = open(temp_file, 'r')
for line in fd_temp.readlines():
    if(">:" in line):
        temp, name1 = line.split('<')
        name, temp = name1.split('>')
        continue
    if("sub	sp, sp, #" in line):
        temp, size1 = line.split('#')
        list_size = size1.split()
        size = int(list_size[0])
        if(size > 1000):
            ws.append([name, size])

fd_temp.close()

ws.auto_filter.ref = 'A:B'
ws.auto_filter.add_sort_condition('B:B')
wb.save(Statics_result_file)







