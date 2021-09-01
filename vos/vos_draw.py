
import tkinter 
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.ttk
#from PIL import Image, ImageTk

class Vosdraw:
    def __init__(self, hroot):
        self.hroot = hroot

    def drawItem(self, item1):
        if item1['type'] == "label":
            labelName = tkinter.Label(self.hroot, text=item1['text'], justify=tkinter.RIGHT,\
                anchor='nw',width=item1['size_wh'][0])
            labelName.place(x=item1['pos_xy'][0], y=item1['pos_xy'][1],\
                width=item1['size_wh'][0], height=item1['size_wh'][1])
            item1['object'] = labelName
            return labelName
        elif item1['type'] == "image":
            img_open = Image.open(item1['option'])
            imag_pic = img_open.resize((100,100))
            image1 = ImageTk.PhotoImage(imag_pic)
            #image1 = tkinter.PhotoImage(file=item1['option'])
            
            imageName = tkinter.Label(self.hroot, image=image1)
            imageName.place(x=item1['pos_xy'][0], y=item1['pos_xy'][1], \
                width=item1['size_wh'][0], height=item1['size_wh'][1])

            item1['object'] = imageName
            return imageName
        elif item1['type'] == "ckbutton": #check button
            item1['option'] = tkinter.IntVar(self.hroot, value=0)
            ckbutton = tkinter.Checkbutton(self.hroot, text=item1['text'], justify='left', variable=item1['option'], onvalue=1, offvalue=0, anchor='nw')
            ckbutton.place(x=item1['pos_xy'][0], y=item1['pos_xy'][1], \
                width=item1['size_wh'][0], height=item1['size_wh'][1])
            item1['object'] = ckbutton
            return ckbutton
        elif item1['type'] == "rdbutton": #radio button
            item1['option'] = tkinter.IntVar(self.hroot, value=0)
            i = 0
            for rdtext in item1['text']:
                rdbutton = tkinter.Radiobutton(self.hroot, variable=item1['option'], value=i, text=rdtext)
                if(item1['direct'] == 'Horizen'):
                    x = item1['pos_xy'][0] + item1['size_wh'][0]*(i%8)
                    y = item1['pos_xy'][1] + item1['size_wh'][1]*(i//8)
                else:
                    x = item1['pos_xy'][0]
                    y = item1['pos_xy'][1] + item1['size_wh'][1]*i
                rdbutton.place(x=x, y=y, width=item1['size_wh'][0], height=item1['size_wh'][1]) # anchor='w')
                i += 1
            item1['object'] = rdbutton
            return rdbutton
        elif item1['type'] == "entry":
            textvar = tkinter.StringVar(value=item1['text'])
            entryName = tkinter.Entry(self.hroot, width=item1['size_wh'][0], textvariable=textvar)
            entryName.place(x=item1['pos_xy'][0], y=item1['pos_xy'][1],\
                width=item1['size_wh'][0], height=item1['size_wh'][1])
            item1['object'] = entryName
            return entryName
        elif item1['type'] == "button":
            buttonName = tkinter.Button(self.hroot, text=item1['text'], command=item1['command'])
            buttonName.place(x=item1['pos_xy'][0], y=item1['pos_xy'][1],\
                width=item1['size_wh'][0], height=item1['size_wh'][1])
            item1['object'] = buttonName
            return buttonName    
        elif item1['type'] == "listbox":
            listName = tkinter.Listbox(self.hroot, selectmod='multiple')
            listName.place(x=item1['pos_xy'][0], y=item1['pos_xy'][1],\
                width=item1['size_wh'][0], height=item1['size_wh'][1])
            item1['object'] = listName
            return listName
        elif item1['type'] == "message":
            msgName = tkinter.Message(self.hroot, bg='black', fg='white', width=item1['size_wh'][0])
            msgName.place(x=item1['pos_xy'][0], y=item1['pos_xy'][1],\
                width=item1['size_wh'][0], height=item1['size_wh'][1])
            item1['object'] = msgName
            return msgName
        elif item1['type'] == "listtext":
            textName = tkinter.scrolledtext.ScrolledText(self.hroot, bg='black', fg='white', width=item1['size_wh'][0], wrap=tkinter.WORD)
            textName.place(x=item1['pos_xy'][0], y=item1['pos_xy'][1],\
                width=item1['size_wh'][0], height=item1['size_wh'][1])
            item1['object'] = textName
            return textName
        elif item1['type'] == "combobox":
            textName = tkinter.ttk.Combobox(self.hroot, values=item1['text'], width=item1['size_wh'][0])
            textName.place(x=item1['pos_xy'][0], y=item1['pos_xy'][1],\
                width=item1['size_wh'][0], height=item1['size_wh'][1])
            item1['object'] = textName
            return textName
            
    def drawList(self, list1):
        for item in list1:
            self.drawItem(item)




