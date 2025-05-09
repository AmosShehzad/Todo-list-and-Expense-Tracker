from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from customtkinter import *
from PIL import Image
from datetime import datetime,time
from tkcalendar import DateEntry
import os
import pygame
import sqlite3 as sq
class todo:
    con = sq.connect('work.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Wrk(Todo text,Date date,Time time)")
    con.commit()
    def __init__(self,root):
        self.root = root
        self.root.attributes('-fullscreen',True)
        self.root.configure(bg="sandy brown")
        self.root.label = Label(
            text="To-Do!\nEnter Data Below...",
            font=("Arial", 30, "bold"),
            fg="white",
            bg="sandy brown")
        self.root.label.pack(padx=50, pady=50)
        self.img = Image.open("C:\\Users\\Administrator\\Desktop\\To-Do Project\\back.png")
        self.toggle_button = CTkButton(self.root,text="Back",border_color="black",border_width=1,
        command=self.back,image=CTkImage(light_image=self.img, dark_image=self.img),width=150,height=50,
        font=("Arial", 16),bg_color="orange",fg_color="orange",hover_color="orange red")
        self.toggle_button.place(x=5, y=10)
        self.fr1 = CTkFrame(master=self.root,fg_color="navajo white",border_width=2,border_color="white",
        width=600,height=400)
        self.fr1.place(relx=0.5,rely=0.5,anchor="center")
        self.lbl3 = CTkLabel(master=self.fr1,text="Enter Work:-",text_color="black",font=("Bold",18))
        self.lbl3.place(relx=0.1,rely=0.1)
        self.e1 = CTkEntry(master=self.fr1,placeholder_text="Enter Work to do",width=250,height=30)
        self.e1.place(relx=0.2,rely=0.2)
        self.lbl1 = CTkLabel(master=self.fr1,text="Select Time:-",text_color="black",font=("Bold",18))
        self.lbl1.place(relx=0.1,rely=0.3)
        self.lbl4 = CTkLabel(master=self.fr1,text="Hour:-",text_color="black",font=("Bold",18))
        self.lbl4.place(relx=0.1,rely=0.4)
        self.cb1 = CTkComboBox(master=self.fr1,width=100,height=30,
        values=["01","02","03","04","05","06","07","08","09","10","11","12"]
        ,fg_color="DarkOrange1",dropdown_fg_color="orange",dropdown_hover_color="orange red",
        button_color="goldenrod2",border_color="goldenrod1")
        self.cb1.place(relx=0.1,rely=0.5)
        self.lbl5 = CTkLabel(master=self.fr1,text="Minute:-",text_color="black",font=("Bold",18))
        self.lbl5.place(relx=0.4,rely=0.4)
        self.cb2 = CTkComboBox(master=self.fr1,width=100,height=30,
        values = [str(i) for i in range(0, 60)]
        ,fg_color="DarkOrange1",dropdown_fg_color="orange",dropdown_hover_color="orange red",
        button_color="goldenrod2",border_color="goldenrod1")
        self.cb2.place(relx=0.4,rely=0.5)
        self.cb3 = CTkComboBox(master=self.fr1,width=100,height=30,
        values = ["AM","PM"]
        ,fg_color="DarkOrange1",dropdown_fg_color="orange",dropdown_hover_color="orange red",
        button_color="goldenrod2",border_color="goldenrod1")
        self.cb3.place(relx=0.6,rely=0.5)
        self.lbl2 = CTkLabel(master=self.fr1,text="Select Date:-",text_color="black",font=("Bold",18))
        self.lbl2.place(relx=0.1,rely=0.6)
        self.c = DateEntry(self.fr1,selectmode="day",date_pattern='dd/MM/yyyy')
        self.c.place(relx=0.3,rely=0.7)
        self.btn2 = CTkButton(master=self.fr1,font=("Arial", 16),bg_color="orange",fg_color="orange",hover_color="orange red",
        text="Submit",border_color="black",border_width=1,width=150,height=50,command=self.ad)
        self.btn2.place(relx=0.35,rely=0.8)
        pygame.mixer.init()
        self.check_alarms()
    def back(self):
        self.root.withdraw()
        os.system("Python3.12 LandingPage.py")
        self.root.destroy()
    def ad(self):
        a = int(self.cb1.get())
        b = int(self.cb2.get())
        c = self.cb3.get()
        d = self.e1.get()
        e = self.c.get()
        t = f"{a}:{b} {c}"
        self.cur.execute("INSERT INTO Wrk(Todo,Date,Time) VALUES(?,?,?)",(d,e,t))
        self.con.commit()
        messagebox.showinfo("Command Executed","Your Data is Submitted")
    def check_alarms(self):
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%d/%m/%Y")
        self.cur.execute("SELECT Todo, Date, Time FROM Wrk")
        tasks = self.cur.fetchall()
        for task in tasks:
            todo, date, time_ = task
            if date == current_date and time_ == current_time:
                pygame.mixer.music.load("alarm.mp3")
                pygame.mixer.music.play()
                self.cur.execute("DELETE FROM Wrk WHERE Todo=? AND Date=? AND Time=?",(todo,date,time_))
                self.con.commit()
        self.root.after(60000, self.check_alarms)
    def __del__(self):
        pygame.mixer.quit()
def t():
    root = Tk()
    obj = todo(root)
    root.mainloop()
t()
