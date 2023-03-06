
from ALU import ALU
from CU import CU
from RAM import RAM
from BUS import Bus
from compiler import compiler

import tkinter as tk
from tkinter import filedialog
import pygubu
import re, os, sys

bus = Bus()
ram = RAM(0x0, 64)
# attaching ram to bus 
bus.AddMemoryPeripheral(ram, 0x0, 0x0+64*1024-1) # mapping address(0-65535 or 0x0000-0xFFFF) to ram

alu = ALU()
cu = CU(alu, bus)
cu.Reset()

def hexStr(n, fill=2):
    """Return hexadecimal representation of 'n' as a string without
    '0x' in the beginning and padded with zeroes to form
    'fill' number of characters"""
    return hex(n).replace('0x','').zfill(fill).upper()

def binStr(n, fill=8):
    """Return binary representation of 'n' as a string without
    '0b' in the beginning and padded with zeroes to form
    'fill' number of characters"""
    return bin(n).replace('0b','').zfill(fill)

def execute():
    try:
        cu.Run()
    except Exception as ex:
        win.Clear()
        print()
        print ("Error: ")
        print ("=======")
        print(ex)
        print("\tat address: " + hex(alu.registers['PC']))
        print()
        cu.Reset()

def WriteMemData(addr, data):
    bus.WriteMemory(addr, data)
def GetMemData(addr):
    return bus.ReadMemory(addr)
def GetRegData(reg):
    return alu.registers[reg]

reglist = [ 'A', 'B', 'C', 'D', 'E', 'H', 'L', 'F' ]
def NextReg(reg):
    return reglist[(reglist.index(reg)+1)%len(reglist)]

def PrevReg(reg):
    id = reglist.index(reg)-1
    if id == -1:
        id = len(reglist) - 1
    return reglist[id]

##################################### GUI Functions  ###############################

# string for reg "  A            00       00000000     000"
# string for flags ""

def on_resetClick():
    alu.Reset()
    update()
    cu.Reset()

def on_runClick():
    alu.registers['PC'] = int(app.builder.tkvariables['pc'].get(),16)
    execute()
    # print(alu.registers)
    # print(binStr(alu.registers['A']))
    # print('sz-a-p-cy')
    # print(binStr(alu.registers['F']))
    update()
    updateMemView()



def on_prevClick():
    fillAddr = app.builder.tkvariables['fillAddress']
    temp = app.builder.tkvariables['mem1'].get()
    f=int(fillAddr.get(),16)
    if(fillAddr.get() == temp):
        f = f-20
    if(f-20<0):
        f=0
    fillAddr.set(hexStr(f,4))
    updateMemView()

def on_nextClick():
    fillAddr = app.builder.tkvariables['fillAddress']
    temp = app.builder.tkvariables['mem1'].get()
    f=int(fillAddr.get(),16)
    if(fillAddr.get() == temp):
        f = f+20
    if(f+20>65535):
        f=65516
    fillAddr.set(hexStr(f,4))
    updateMemView()

def on_fillClick():
    fillAddr = app.builder.tkvariables['fillAddress'].get()
    #app.builder.tkvariables['pc'].set(fillAddr)
    a=int(fillAddr,16)
    d=int(app.builder.tkvariables['val1'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val2'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val3'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val4'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val5'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val6'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val7'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val8'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val9'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val10'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val11'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val12'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val13'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val14'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val15'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val16'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val17'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val18'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val19'].get(),16);WriteMemData(a,d)
    a=a+1;d=int(app.builder.tkvariables['val20'].get(),16);WriteMemData(a,d)
    
def on_loadClick():
    la = app.builder.tkvariables['loadAddr'].get()
    loadAddr = int(la,16)
    codestr = app.builder.get_object('Text_1').get('1.0', tk.END+"-1c")
    codelines = codestr.split('\n')
    for codeline in codelines:
        opcodes = compiler(codeline)
        for x in opcodes:
            WriteMemData(loadAddr,x)
            loadAddr=loadAddr+1
    app.builder.tkvariables['pc'].set(la)
    app.builder.tkvariables['fillAddress'].set(la)
    updateMemView()

def on_saveClick():
    fileName = app.builder.tkvariables['fileName'].get()
    codestr = app.builder.get_object('Text_1').get('1.0', tk.END+"-1c")
    with open("yourcodes/"+fileName+".txt", 'w+') as f:
        f.write(codestr)

def on_loadfileClick():
    fileName = filedialog.askopenfilename(title='select file',filetypes=(('textfiles', '*.txt'),('All files', '*.*')))
    with open(fileName,'r') as f:
        codestr = f.read()
        t = app.builder.get_object('Text_1')
        t.delete(1.0, tk.END)
        t.insert(tk.END, codestr)
    i=fileName.rindex('/')+1
    app.builder.tkvariables['fileName'].set(fileName[i:])

def on_clearClick():
    app.builder.get_object('Text_1').delete(1.0, tk.END)


def update():
    a_val = alu.registers['A']
    app.builder.tkvariables['regA'].set("  A            "+hexStr(a_val)+"       "+binStr(a_val)+"     "+str(a_val).zfill(3))
    b_val = alu.registers['B']
    app.builder.tkvariables['regB'].set("  B            "+hexStr(b_val)+"       "+binStr(b_val)+"     "+str(b_val).zfill(3))
    c_val = alu.registers['C']
    app.builder.tkvariables['regC'].set("  C            "+hexStr(c_val)+"       "+binStr(c_val)+"     "+str(c_val).zfill(3))
    d_val = alu.registers['D']
    app.builder.tkvariables['regD'].set("  D            "+hexStr(d_val)+"       "+binStr(d_val)+"     "+str(d_val).zfill(3))
    e_val = alu.registers['E']
    app.builder.tkvariables['regE'].set("  E            "+hexStr(e_val)+"       "+binStr(e_val)+"     "+str(e_val).zfill(3))
    f_val = alu.registers['F']
    app.builder.tkvariables['regF'].set("  F            "+hexStr(f_val)+"       "+binStr(f_val)+"     "+str(f_val).zfill(3))
    h_val = alu.registers['H']
    app.builder.tkvariables['regH'].set("  H            "+hexStr(h_val)+"       "+binStr(h_val)+"     "+str(h_val).zfill(3))
    l_val = alu.registers['L']
    app.builder.tkvariables['regL'].set("  L            "+hexStr(l_val)+"       "+binStr(l_val)+"     "+str(l_val).zfill(3))
    sp_val = alu.registers['SP']
    app.builder.tkvariables['regSP'].set("SP : 0x"+hexStr(sp_val,4))

    flagStr = binStr(f_val)
    app.builder.tkvariables['sFlag'].set(" S   :  "+flagStr[0])
    app.builder.tkvariables['zFlag'].set(" Z   :  "+flagStr[1])
    app.builder.tkvariables['acFlag'].set(" AC :  "+flagStr[3])
    app.builder.tkvariables['pFlag'].set(" P   :  "+flagStr[5])
    app.builder.tkvariables['cyFlag'].set(" AC :  "+flagStr[7])

def updateMemView():
    startAddr = int(app.builder.tkvariables['fillAddress'].get(),16)
    app.builder.tkvariables['mem1'].set(hexStr(startAddr,4))
    app.builder.tkvariables['mem2'].set(hexStr(startAddr+1,4))
    app.builder.tkvariables['mem3'].set(hexStr(startAddr+2,4))
    app.builder.tkvariables['mem4'].set(hexStr(startAddr+3,4))
    app.builder.tkvariables['mem5'].set(hexStr(startAddr+4,4))
    app.builder.tkvariables['mem6'].set(hexStr(startAddr+5,4))
    app.builder.tkvariables['mem7'].set(hexStr(startAddr+6,4))
    app.builder.tkvariables['mem8'].set(hexStr(startAddr+7,4))
    app.builder.tkvariables['mem9'].set(hexStr(startAddr+8,4))
    app.builder.tkvariables['mem10'].set(hexStr(startAddr+9,4))
    app.builder.tkvariables['mem11'].set(hexStr(startAddr+10,4))
    app.builder.tkvariables['mem12'].set(hexStr(startAddr+11,4))
    app.builder.tkvariables['mem13'].set(hexStr(startAddr+12,4))
    app.builder.tkvariables['mem14'].set(hexStr(startAddr+13,4))
    app.builder.tkvariables['mem15'].set(hexStr(startAddr+14,4))
    app.builder.tkvariables['mem16'].set(hexStr(startAddr+15,4))
    app.builder.tkvariables['mem17'].set(hexStr(startAddr+16,4))
    app.builder.tkvariables['mem18'].set(hexStr(startAddr+17,4))
    app.builder.tkvariables['mem19'].set(hexStr(startAddr+18,4))
    app.builder.tkvariables['mem20'].set(hexStr(startAddr+19,4))

    app.builder.tkvariables['val1'].set(hexStr(GetMemData(startAddr)))
    app.builder.tkvariables['val2'].set(hexStr(GetMemData(startAddr+1)))
    app.builder.tkvariables['val3'].set(hexStr(GetMemData(startAddr+2)))
    app.builder.tkvariables['val4'].set(hexStr(GetMemData(startAddr+3)))
    app.builder.tkvariables['val5'].set(hexStr(GetMemData(startAddr+4)))
    app.builder.tkvariables['val6'].set(hexStr(GetMemData(startAddr+5)))
    app.builder.tkvariables['val7'].set(hexStr(GetMemData(startAddr+6)))
    app.builder.tkvariables['val8'].set(hexStr(GetMemData(startAddr+7)))
    app.builder.tkvariables['val9'].set(hexStr(GetMemData(startAddr+8)))
    app.builder.tkvariables['val10'].set(hexStr(GetMemData(startAddr+9)))
    app.builder.tkvariables['val11'].set(hexStr(GetMemData(startAddr+10)))
    app.builder.tkvariables['val12'].set(hexStr(GetMemData(startAddr+11)))
    app.builder.tkvariables['val13'].set(hexStr(GetMemData(startAddr+12)))
    app.builder.tkvariables['val14'].set(hexStr(GetMemData(startAddr+13)))
    app.builder.tkvariables['val15'].set(hexStr(GetMemData(startAddr+14)))
    app.builder.tkvariables['val16'].set(hexStr(GetMemData(startAddr+15)))
    app.builder.tkvariables['val17'].set(hexStr(GetMemData(startAddr+16)))
    app.builder.tkvariables['val18'].set(hexStr(GetMemData(startAddr+17)))
    app.builder.tkvariables['val19'].set(hexStr(GetMemData(startAddr+18)))
    app.builder.tkvariables['val20'].set(hexStr(GetMemData(startAddr+19)))

##########################################   GUI   #####################################

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('8085.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainFrame', master)

callbacks = {
    'runClicked' : on_runClick,
    'resetClicked': on_resetClick,
    'prevClicked' : on_prevClick,
    'nextClicked' : on_nextClick,
    'fillClicked': on_fillClick,
    'loadClicked' : on_loadClick,
    'saveClicked' : on_saveClick,
    'loadfileClicked' : on_loadfileClick,
    'clearClicked' : on_clearClick
}

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.builder.connect_callbacks(callbacks)
    root.resizable(width=False, height=False)
    root.title(string='8085')
    root.mainloop()
