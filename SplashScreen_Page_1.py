from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import os

root = Tk()
image = "C:\\Users\\Administrator\\Desktop\\To-Do Project\\abc2.png"  
image = PhotoImage(file=image)   

height = 430
width = 530

root.config(background="sandy brown")
root.attributes('-fullscreen', True)

wlabel = Label(text="Hello Champ!", bg="sandy brown", fg="white", font=("Trebuchet Ms", 24, "bold"))
wlabel.place(x=520, y=40)

blabel = Label(root, image=image, bg="sandy brown")
blabel.place(x=400, y=130)

plabel = Label(root, text="Loading......", bg="sandy brown", fg="white", font=("Trebuchet Ms", 24, "bold"))
plabel.place(x=540, y=600)

style = ttk.Style()
style.theme_use('clam')
style.configure('red.Horizontal.TProgressbar', troughcolor='white', background='coral', thickness=20)

progress = Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate',
style='red.Horizontal.TProgressbar')
progress.place(x=430, y=670)
progress_label =Label(text="Start")
def top():
    root.withdraw
    os.system("Python3.12 LandingPage.py")
    root.destroy()
i = 0
def load():
    global i
    if i<=10:
        txt = "Loading....."+str(10*i)+"%"
        progress_label.config(text=txt)
        progress_label.after(600,load)
        progress['value'] = 10*i
        i += 1
    else:
        top()
load()
root.mainloop()
