from tkinter import *
from tkinter import messagebox
from customtkinter import *
from PIL import Image
from tkinter import messagebox
import sqlite3 as sq
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import pygame
from datetime import datetime

class exp:
    con = sq.connect("expense.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Exp(Name TEXT, spent INTEGER)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS Wrk(Todo text,Date date,Time time)")
    con.commit()

    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="sandy brown")

        self.root.label = Label(
            text="Expense Chart!",font=("Arial", 30, "bold"),fg="white",bg="sandy brown")
        self.root.label.pack(padx=50, pady=50)

        self.img = Image.open("C:\\Users\\Administrator\\Desktop\\To-Do Project\\back.png")
        self.toggle_button = CTkButton(
            self.root,
            text="Back",
            border_color="black",
            border_width=1,
            command=self.back,
            image=CTkImage(light_image=self.img, dark_image=self.img),width=150,height=50,
            font=("Arial", 16),bg_color="orange",fg_color="orange",hover_color="orange red")
        self.toggle_button.place(x=5, y=10)

        self.btn2 = CTkButton(
            master=self.root,
            text="Add Expenses", width=150,height=50,fg_color="orange",bg_color="orange",
            hover_color="orange red",border_width=1,border_color="black",command=self.btn)
        self.btn2.place(x=350, y=600)
        
        self.btn3 = CTkButton(
            master=self.root,
            text="Delete Expense",
            width=150,height=50,fg_color="orange",bg_color="orange",hover_color="orange red",
            border_width=1,border_color="black",command=self.dd)
        self.btn3.place(x=800, y=600)

        self.check_and_reset_data()
        self.graph()
        self.monS()
        pygame.mixer.init()
        self.check_alarms()
    
    def dd(self):
        if hasattr(self, "entry_form") and self.entry_form.winfo_exists():
            self.entry_form.pack_forget()

        if hasattr(self, "df") and self.df.winfo_exists():
            self.df.lift()
            return

        self.df = CTkFrame(master=self.root, width=600, height=400, bg_color="yellow", fg_color="orange")
        self.df.pack()
        self.de = CTkEntry(master=self.df, placeholder_text="Enter Name of Expense ", width=150, height=50)
        self.de.pack()
        self.dbtn = CTkButton(
            master=self.df, text="Delete", width=80,
            text_color="black", height=30, font=("Arial", 12),
            bg_color="orange", fg_color="orange",
            hover_color="dark orange", command=self.dframe
        )
        self.dbtn.pack()
        self.dbtn1 = CTkButton(
            master=self.df, text="Cancel", width=80,
            text_color="black", height=30, font=("Arial", 12),
            bg_color="orange", fg_color="orange",
            hover_color="dark orange", command=self.df.destroy
        )
        self.dbtn1.pack()
    
    def dframe(self):
        z = self.de.get()
        if not z.isalpha():
            messagebox.showerror("Error", "Enter Valid Input")
            return
        else:
            self.cur.execute("DELETE FROM Exp WHERE Name=?", (z,))
            self.con.commit()
            self.update_graph()
        self.de.delete(0, END)
        self.df.destroy()
    
    def add(self, name, spent):
        self.cur.execute("INSERT INTO Exp(Name, spent) VALUES(?, ?)", (name, spent))
        self.con.commit()
     
    def monS(self):
        self.s = CTkFrame(
            master=self.root, width=600, height=400,
            fg_color="yellow", bg_color="white",
            border_width=3, border_color="black"
        )
        self.s.place(x=900, y=250)

        self.cur.execute("SELECT SUM(spent) FROM Exp")
        total_spent = self.cur.fetchone()[0]
        if total_spent is None:
            total_spent = 0

        self.lbl = CTkLabel(
            master=self.s, text=f"Total Money Spent:\n{total_spent} RS",
            font=("Bold", 20), width=250, height=150
        )
        self.lbl.pack()

    def btn(self):
        if hasattr(self, "df") and self.df.winfo_exists():
            self.df.pack_forget()

        if hasattr(self, 'entry_form') and self.entry_form.winfo_exists():
            self.entry_form.lift()
            return

        self.entry_form = CTkFrame(master=self.root, bg_color="yellow", fg_color="orange", width=300, height=200)
        self.entry_form.pack()

        self.cb = CTkEntry(master=self.entry_form, placeholder_text="Enter Expense:")
        self.cb.pack()

        self.cb1 = CTkEntry(master=self.entry_form, placeholder_text="Enter Money spent:")
        self.cb1.pack()

        self.b = CTkButton(
            master=self.entry_form, width=80, text_color="black", text="Submit",
            height=30, font=("Arial", 12), bg_color="orange",
            fg_color="orange", hover_color="dark orange",
            command=self.submit_form
        )
        self.b.pack()

        self.b1 = CTkButton(
            master=self.entry_form, width=80, text_color="black", text="Cancel",
            height=30, font=("Arial", 12), bg_color="orange",
            fg_color="orange", hover_color="dark orange",
            command=self.entry_form.destroy
        )
        self.b1.pack()

    def submit_form(self):
        expense = self.cb.get()
        money_spent = self.cb1.get()

        if not expense.isalpha() or not expense.strip():
            messagebox.showerror("Error", "Enter Valid Input")
            return

        if not money_spent.isdigit() and money_spent is None:
            messagebox.showerror("Error", "Enter Valid Input")
            return

        self.add(expense, money_spent)
        self.update_graph()

        self.cb.delete(0, END)
        self.cb1.delete(0, END)
        self.entry_form.destroy()

    def graph(self):
        self.fr = CTkFrame(
            master=self.root, width=450, height=350,
            fg_color="white", bg_color="sandy brown",
            border_width=1, border_color="black"
        )
        self.fr.pack(padx=20, pady=20)

        self.update_graph()

    def update_graph(self):
        for widget in self.fr.winfo_children():
            widget.destroy()

        self.cur.execute("SELECT Name, spent FROM Exp")
        data = self.cur.fetchall()

        if data:
            labels, values = zip(*data)
        else:
            labels, values = [], []

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(values, labels=labels, autopct='%2.2f%%')

        canvas = FigureCanvasTkAgg(fig, master=self.fr)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def check_and_reset_data(self):
        current_day = datetime.now().day

        if current_day == 1:
            self.cur.execute("DELETE FROM Exp")
            self.con.commit()
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

    def back(self):
        self.root.withdraw()
        os.system("Python3.12 LandingPage.py")
        self.root.destroy()

def expense():
    root = Tk()
    obj = exp(root)
    root.mainloop()
expense()
