from tkinter import *
from tkinter import messagebox
import Images
import time
import threading
import base64
import os
import inspect
import ctypes

sudoku = [0 for i in range(81)]
tempNum = [0 for i in range(81)]
tempSp = 0
startH = [0 for i in range(81)]
startV = [0 for i in range(81)]
startB = [0 for i in range(81)]
addH = [0 for i in range(9)]
addV = [0 for i in range(9)]
addB = [0 for i in range(9)]
L = 'LightBlue'
C = 'cornsilk'
Color = [L, L, L, C, C, C, L, L, L,
         L, L, L, C, C, C, L, L, L,
         L, L, L, C, C, C, L, L, L,
         C, C, C, L, L, L, C, C, C,
         C, C, C, L, L, L, C, C, C,
         C, C, C, L, L, L, C, C, C,
         L, L, L, C, C, C, L, L, L,
         L, L, L, C, C, C, L, L, L,
         L, L, L, C, C, C, L, L, L]

store = [False for i in range(81)]

def printSudoku():
    global sudoku
    for i in range(81):
        print('%2d' % sudoku[i], end='')
        if i % 9 == 8:
            print()

def init():
    global addB, addH, addV, startB, startV, tempSp
    tempSp = 0
    for i in range(81):
        startH[i] = i // 9 * 9
        startV[i] = i % 9
        startB[i] = i // 9 // 3 * 27 + i % 9 // 3 * 3

    for i in range(9):
        addH[i] = i
        addV[i] = i * 9
        addB[i] = i // 3 * 9 + i % 3

    print('init done')


def getNextBlank(sp):
    while 1:
        sp += 1
        if not (sp < 81 and sudoku[sp] > 0):
            break

    return sp


def Push(sp):
    global tempNum
    global tempSp
    tempNum[tempSp] = sp
    tempSp += 1


def Pop():
    global tempSp
    if tempSp <= 0:
        return -1
    else:
        tempSp -= 1
        return tempNum[tempSp]


def check1(sp, start, addNum):
    fg = 0
    for i in range(9):
        sp1 = start + addNum[i]
        if sp != sp1 and sudoku[sp] == sudoku[sp1]:
            fg += 1

    return fg


def check(sp):
    fg = 0
    if fg == 0:
        fg = check1(sp, startH[sp], addH)
    if fg == 0:
        fg = check1(sp, startV[sp], addV)
    if fg == 0:
        fg = check1(sp, startB[sp], addB)
    return fg


def tryAns():
    sp = getNextBlank(-1)
    while 1:
        if not (sp >= 0 and sp < 81):
            break
        sudoku[sp] += 1
        if sudoku[sp] > 9:
            sudoku[sp] = 0
            sp = Pop()
        elif check(sp) == 0:
            Push(sp)
            sp = getNextBlank(sp)

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
win.title('SUDOKU')
win.geometry('650x800')
win.resizable(0, 0)
win.protocol('WM_DELETE_WINDOW', closeWindow)

Start = Images.img1
S = PhotoImage(data=Start)

Clear = Images.img2
C = PhotoImage(data=Clear)

Type1 = Images.img3
T1 = PhotoImage(data=Type1)

Type2 = Images.img4
T2 = PhotoImage(data=Type2)

num = []
entrys = []

for i in range(81):
    e = StringVar()
    num.append(e)

def test(content):
    print(content)
    if content.isdigit() or content == '':
        if len(content) <= 1:
            return True
        return False
    else:
        return False

test_cmd = win.register(test)
num = []
for i in range(81):
    e = StringVar()
    num.append(e)

entrys = []
x = 0
for i in range(9):
    for j in range(9):
        e = Entry(master=win, width=3, font=("Helvetica", "21", "bold"), justify='center', 
            textvariable=num[x], bg=Color[x], cursor='sizing', validate='key', validatecommand=(test_cmd, '%P'))
        e.grid(row=i, column=j, padx=9, pady=10)
        entrys.append(e)
        x += 1

frames = [PhotoImage(data=s) for s in Images.proc]
Len = len(frames)
def update(ind):
    global win, label_processing
    frame = frames[ind]
    ind += 1
    if ind == Len:
        ind = 0
    label_processing.configure(image=frame)
    win.after(50, update, ind)
label_processing = Label(master=win)
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

def write():
    for i in range(81):
        if sudoku[i] != 0:
            num[i].set(str(sudoku[i]))

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
    global b1, b2, label_processing, entrys
    b1.configure(state="disable")
    b2.configure(state="disable")
    for e in entrys:
        e.configure(state="disable")
    label_processing.place(x=170, y=100, anchor='nw')  
    start_time = time.time()
    tryAns()
    end_time = time.time()
    label_processing.place_forget()
    run_time = end_time - start_time
    Time = round(run_time * 1000) / 1000
    show()
    messagebox.showinfo("Good!", "Solved!\nTime spent: " + str(Time) + " seconds")
    b1.configure(state="normal")
    b2.configure(state="normal")
    for e in entrys:
        e.configure(state="normal")

def go():
    global t
    read()
    if full():     
        messagebox.showinfo("", "Already solved!")
        return
    init()
    t = threading.Thread(target=do_sudoku)
    t.setDaemon(True)
    t.start() 

def cl():
    global sudoku, num, store, entrys
    for i in range(81):
        num[i].set("")
        store[i] = False
        entrys[i].configure(fg="black")
        sudoku[i] = 0

def keyIn():
    print("input")

class MyDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.resizable(0, 0)
        top.wm_geometry("300x430")
        top.attributes('-topmost', 'true')
        top.wait_visibility()
        top.grab_set()
        top.wm_title('key in')
        top.focus()

        self.myTextBox = Text(top, font=("Helvetica", "20", "bold"), height=9, width=9, padx=0)
        self.myTextBox.pack()

        self.myOkButton = Button(top, text='Ok', command=self.ok)
        self.myOkButton.pack()

        self.myCancelButton = Button(top, text='Cancel', command=self.cancel)
        self.myCancelButton.pack()

    def ok(self):
        global num
        print('ok')
        temp = self.myTextBox.get(1.0, END)
        print(temp)
        index = 0
        for ch in temp:
            if ch in '123456789':
                num[index].set(ch)
                index += 1
            elif ch == '0':
                index += 1
            if index == 81:
                break

        self.top.destroy()

    def cancel(self):
        print('cancel')
        self.top.destroy()

def create_new_windows():
    print("new windows")
    inputDialog = MyDialog(win)
    win.wait_window(inputDialog.top)

class myLabel(Label):    
    def __init__(self, master=None, image=None, cursor=None):
        Label.__init__(self, master)
        Label.config(self, image=image, cursor=cursor)
        self.img = image
        self.createWidgets()
    def mouseEnter(self, event):
        self.config(image=T2)
    def mouseLeave(self, event):
        self.config(image=T1)
    def mouseClick(self, event):
        create_new_windows()
    def createWidgets(self):    
        self.bind("<Enter>", self.mouseEnter)
        self.bind("<Leave>", self.mouseLeave)
        self.bind("<Button-1>", self.mouseClick)

b1 = Button(master=win, image=S, command=go, cursor='star')
b1.place(x=45, y=580, anchor='nw')
b2 = Button(master=win, image=C, command=cl, cursor='pirate')
b2.place(x=325, y=580, anchor='nw')
tb = myLabel(master=win, image=T1, cursor='target')
tb.place(x=260, y=700, anchor='nw')
write()
win.mainloop()