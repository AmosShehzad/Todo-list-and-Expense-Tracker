from tkinter import *
from tkinter import ttk
from customtkinter import *
from PIL import Image
from tkinter import messagebox
import os
import sys
import sqlite3 as sq
import pygame
from datetime import datetime
class page:
    con = sq.connect('work.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Wrk(Todo text,Date date,Time time)")
    con.commit()
    def __init__(self,root):
        self.root = root
        self.root.title("TO-Do")
        root.attributes('-fullscreen', True)
        self.root.configure(bg="sandy brown")
        self.root.label = Label(text="Welome to Your To-Do!",font=("Arial",30,"bold"),fg="white",bg="sandy brown")
        self.root.label.pack(padx=50,pady=50)
        self.img = Image.open("C:\\Users\\Administrator\\Desktop\\To-Do Project\\on.png")
        self.img1 = Image.open("C:\\Users\\Administrator\\Desktop\\To-Do Project\\close.png")
        self.img2 = Image.open("C:\\Users\\Administrator\\Desktop\\To-Do Project\\todo.png")
        self.img3 = Image.open("C:\\Users\\Administrator\\Desktop\\To-Do Project\\expense.png")
        self.img4 = Image.open("C:\\Users\\Administrator\\Desktop\\To-Do Project\\quit.png")
        self.toggle_button = CTkButton(self.root,text="Menu"
        ,border_color="black",border_width=1,command=self.toogle,
        image=CTkImage(light_image=self.img,dark_image=self.img),width=150,height=50,font=("Arial",16),
        bg_color="orange",fg_color="orange",hover_color="orange red")
        self.toggle_button.place(x=5, y=10)
        self.tree() 
        pygame.mixer.init()
        self.check_alarms()
    def toogle(self):
        self.f1 = CTkFrame(self.root, width=250, height=550,fg_color="peach puff",
        bg_color="peach puff",border_color="white",border_width=2)
        self.f1.place(x=0, y=0)
        self.b1 = CTkButton(self.f1,width=140,height=50,font=("Arial",18),bg_color="orange",
        fg_color="orange",hover_color="orange red",border_color="black",border_width=1,
        image=CTkImage(light_image=self.img2,dark_image=self.img2), text="To-Do", command=self.td)
        self.b1.place(x=50, y=100)
        self.b2 = CTkButton(self.f1,width=140,height=50,font=("Arial",18),bg_color="orange",
        fg_color="orange",hover_color="orange red",border_color="black",border_width=1,
        image=CTkImage(light_image=self.img3,dark_image=self.img3), text="Expense\nTracker", command=self.exp)
        self.b2.place(x=50, y=200)
        self.b3 = CTkButton(self.f1,width=140,height=50,font=("Arial",18),bg_color="orange",
        fg_color="orange",hover_color="orange red",border_color="black",border_width=1,
        image=CTkImage(light_image=self.img4,dark_image=self.img4), text="Quit", command=self.quit_action)
        self.b3.place(x=50, y=300)
        close_button = CTkButton(self.f1,width=140,height=50,font=("Arial",18),bg_color="orange",
        fg_color="orange",hover_color="orange red",border_color="black",border_width=1,
        image=CTkImage(light_image=self.img1,dark_image=self.img1), text="Close", command=self.f1.destroy)
        close_button.place(x=5, y=5)
    def quit_action(self):
        sys.exit() 
    def exp(self):
        self.root.withdraw()
        os.system("Python3.12 Expense.py")
        self.root.destroy()
    def td(self):
        self.root.withdraw()
        os.system("Python3.12 To-Do.py")
        self.root.destroy()
    def tree(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview",background="blue",foreground="black",rowheight=30,fieldbackground="white")
        self.style.map('Treeview',background=[('selected','orange red')])
        self.treeframe = Frame(self.root)
        self.treeframe.pack()
        self.treescroll = Scrollbar(self.treeframe)
        self.treescroll.pack(side=RIGHT,fill=Y)
        self.mytree = ttk.Treeview(self.treeframe,yscrollcommand=self.treescroll.set,selectmode="extended")
        self.treescroll.config(command=self.mytree.yview)
        self.mytree.pack()
        self.mytree['column'] = ("To-Do","Date","Time")
        self.mytree.column("#0",width=0,stretch=NO)
        self.mytree.column("To-Do",width=140,anchor=W)
        self.mytree.column("Date",width=140,anchor=CENTER)
        self.mytree.column("Time",width=140,anchor=W)
        self.mytree.heading("#0",text='',anchor=CENTER)
        self.mytree.heading("To-Do",text='To-Do',anchor=W)
        self.mytree.heading("Date",text='Date',anchor=CENTER)
        self.mytree.heading("Time",text='Time',anchor=W)
        self.mytree.tag_configure('oddrow',background="goldenrod1")
        self.mytree.tag_configure('evenrow',background="goldenrod2")
        self.cur.execute("SELECT * FROM Wrk")
        w = self.cur.fetchall()
        count=0
        for wk in w:
            if count%2==0:
                self.mytree.insert(parent='',index='end',iid=count,text='',values=(wk[0],wk[1],wk[2]), tags=('evenrow',))
            else:
                self.mytree.insert(parent='',index='end',iid=count,text='',values=(wk[0],wk[1],wk[2]), tags=('oddrow',))
            count +=1
    def check_alarms(self):
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%d/%m/%Y")
        self.cur.execute("SELECT Todo, Date, Time FROM Wrk")
        tasks = self.cur.fetchall()
        for task in tasks:
            todo,date,time_ = task
            if date == current_date or time_ == current_time:
                pygame.mixer.music.load("alarm.mp3")
                pygame.mixer.music.play()
                print(f"{current_time},{time_}")
                messagebox.showinfo("Attention","It's time to Work")
                self.cur.execute("DELETE FROM Wrk WHERE Todo=? AND Date=? AND Time=?",(todo,date,time_))
                self.con.commit()
        self.root.after(60000, self.check_alarms)
    def __del__(self):
        pygame.mixer.quit()
def p():
    root = Tk()
    obj = page(root)
    root.mainloop()
p()