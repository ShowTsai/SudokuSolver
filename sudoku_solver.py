from tkinter import *
from tkinter import messagebox
import Images
import time
import threading
import base64
import os
import inspect
import ctypes

#sudoku
sudoku = [0 for i in range(81)]
tempNum = [0 for i in range(81)]
tempSp = 0
startH = [0 for i in range(81)]
startV = [0 for i in range(81)]
startB = [0 for i in range(81)]
addH = [0 for i in range(9)]
addV = [0 for i in range(9)]
addB = [0 for i in range(9)]

def init():
    global startH, startV, startB, addH, addV, addB, tempSp
    tempSp = 0
    for i in range(81):
        startH[i] = i//9 * 9     
        startV[i] = i % 9              
        startB[i] = ((i//9)//3)*27 + ((i%9)//3)*3
    for i in range(9):
        addH[i] = i                           
        addV[i] = i*9                        
        addB[i] = (i//3)*9 + (i%3)

def tryAns():
    global sudoku
    sp = getNextBlank(-1)
    while True:
        sudoku[sp] += 1
        if sudoku[sp] > 9:
            sudoku[sp] = 0
            sp = pop()
        else:
            if check(sp) == 0:
                push(sp)                      
                sp = getNextBlank(sp)
        if not(sp >= 0 and sp < 81):
            break

def getNextBlank(sp):
    global sudoku
    while True:
        sp += 1
        if not(sp < 81 and sudoku[sp] > 0):
            break
    return sp

def check(sp):
    global startH, startV, startB, addH, addV, addB
    fg = 0
    if fg == 0:
        fg = check1(sp, startH[sp], addH)
    if fg == 0:
        fg = check1(sp, startV[sp], addV)
    if fg == 0:
        fg = check1(sp, startB[sp], addB)
    return fg

def check1(sp, start, addNum):
    global sudoku
    fg = 0
    for i in range(9):
        sp1 = start + addNum[i]
        if sp != sp1 and sudoku[sp] == sudoku[sp1]:
            fg += 1
    return fg

def push(sp):
    global tempNum, tempSp
    tempNum[tempSp] = sp
    tempSp += 1

def pop():
    global tempNum, tempSp
    if tempSp <= 0:
        return -1
    else:
        tempSp -= 1
        return tempNum[tempSp]

#gui
def get_screen_size(window):
    return window.winfo_screenwidth(),window.winfo_screenheight()
 
def get_window_size(window):
    return window.winfo_reqwidth(),window.winfo_reqheight()
 
def center_window(root, width, height):
    screenwidth, screenheight = get_screen_size(root)
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        return
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

t = None

def closeWindow():
    global t
    ans = messagebox.askyesno(title="Warning!", message="Are you sure to close the window?")
    if ans:
        if t != None:
            _async_raise(t.ident, SystemExit)
        win.destroy()
    else:
        return

win = Tk()
win.title("Sudoku Solver")
center_window(win, 700, 700)
win.resizable(False, False)
win.protocol('WM_DELETE_WINDOW', closeWindow)

from icon import Icon
with open('tmp.ico','wb') as tmp:
    tmp.write(base64.b64decode(Icon().img))
win.iconbitmap('tmp.ico')
os.remove('tmp.ico')

A = "#FCF3B8"
B = "#B6FCFA"
color = [A,A,A,B,B,B,A,A,A,
         A,A,A,B,B,B,A,A,A,
         A,A,A,B,B,B,A,A,A,
         B,B,B,A,A,A,B,B,B,
         B,B,B,A,A,A,B,B,B,
         B,B,B,A,A,A,B,B,B,
         A,A,A,B,B,B,A,A,A,
         A,A,A,B,B,B,A,A,A,
         A,A,A,B,B,B,A,A,A]

store = [False for i in range(81)]

num = []
entrys = []

for i in range(81):
    e = StringVar()
    num.append(e)

def test(content):
    if content.isdigit() or content == "":
        if len(content) <= 1:
            return True
        else:
            return False
    else:
        return False

test_cmd = win.register(test)

x = 0
a = 17
for i in range(9):
    b = 15
    for j in range(9):        
        e = Entry(master=win, textvariable=num[x], bg=color[x], width=3,
                  font=("Helvetica", "21", "bold"), justify="center",
                  validate='key', validatecommand=(test_cmd, '%P'))
        e.place(x=a, y=b, anchor='nw')
        entrys.append(e)
        x += 1
        b += 60
    a += 75

Start = Images.img1
S = PhotoImage(data=Start)

Clear = Images.img2
C = PhotoImage(data=Clear)

frames = [PhotoImage(data=s) for s in Images.proc]
Len = len(frames)
def update(ind):
    global win
    frame = frames[ind]
    ind += 1
    if ind == Len:
        ind = 0
    label.configure(image=frame)
    win.after(50, update, ind)
label = Label(master=win)
win.after(0, update, 0)

def read():
    global num, sudoku, store, entrys 
    for i in range(81):
        s = num[i].get()
        if s == "":
            sudoku[i] = 0
            store[i] = True
            entrys[i].configure(fg="red")
        else:
            sudoku[i] = int(s)
            store[i] = False
            entrys[i].configure(fg="black")

def show():
    global num, sudoku
    for i in range(81):
        num[i].set(str(sudoku[i]))

def full():
    global sudoku
    for i in range(81):
        if sudoku[i] == 0:
            return False
    return True

def do_sudoku():
    global b1, b2, label, entrys
    b1.configure(state="disable")
    b2.configure(state="disable")
    for e in entrys:
        e.configure(state="disable")
    label.place(x=200, y=100, anchor='nw')  
    start_time = time.time()
    tryAns()
    end_time = time.time()
    label.place_forget()
    run_time = end_time - start_time
    Time = round(run_time * 1000) / 1000
    show()
    messagebox.showinfo("Good!", "Solved!\nTime spent: " + str(Time) + " seconds")
    b1.configure(state="normal")
    b2.configure(state="normal")
    for e in entrys:
        e.configure(state="normal")

def _start():
    global t
    read()
    if full():     
        messagebox.showinfo("", "Already solved!")
        return
    init()
    t = threading.Thread(target = do_sudoku)
    t.start() 

def _clear():
    global sudoku, num, store, entrys
    for i in range(81):
        num[i].set("")
        store[i] = False
        entrys[i].configure(fg="black")
        sudoku[i] = 0

b1 = Button(master=win, image=S, command=_start)
b1.place(x=70, y=570, anchor='nw')

b2 = Button(master=win, image=C, command=_clear)
b2.place(x=380, y=570, anchor='nw')

win.mainloop()