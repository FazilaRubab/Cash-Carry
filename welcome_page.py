# ----------------------- IMPORT TKINTER LIBRARY 
from tkinter import *
from tkinter import ttk,messagebox
import tkinter as tk
import tkinter
from datetime import datetime
from datetime import date
# -------------- Import Pillow library for images
from PIL import  ImageTk, Image, ImageFilter
import os

# ---------------------- page setting
welcomePage = Tk()
width, height = welcomePage.winfo_screenwidth(), welcomePage.winfo_screenheight()
welcomePage.geometry('%dx%d+0+0' % (width,height))
welcomePage.configure(background="#222A35")
welcomePage.title("Cash & Carry")
welcomePage.resizable(False, False)


# ---------------------- ------------------set icon
p1 = PhotoImage(file = 'images\\back.PNG')
# ---------------------- Setting icon of master window
welcomePage.iconphoto(False, p1)

# ======================================= Back Ground image ================
img5 = Image.open("images\\bgm1.png")
# resize the image and apply a high-quality down sampling filter
img5 = img5.resize((width,height), Image.Resampling.LANCZOS)
# PhotoImage class is used to add image to widgets, icons etc
img5 = ImageTk.PhotoImage(img5)
# create a label
admin_manual_logo = Label(welcomePage, image = img5, bg='#222A35')
# set the image as img
admin_manual_logo.image = img5
admin_manual_logo.place(height=height,width=width,x=0, y=0)




#functions
def admin_func():
    welcomePage.withdraw()
    os.system("python adminLogin.py")
    welcomePage.deiconify()

def employee_func():
    welcomePage.withdraw()
    os.system("python empLogin.py")
    welcomePage.deiconify()



empButton= Button(welcomePage,bd=0,bg="#fffffF" ,font=("times new roman", 18, "bold"),command=employee_func,text='User',activebackground='#ffffff')
empButton.place(height=40,width=160,x=width/3,y=460)


admButton= Button(welcomePage,bd=0,bg="#ffffff", font=("times new roman", 18, "bold") ,command=admin_func,text='Admin',activebackground='#ffffff')
admButton.place(height=40,width=160,x=width/1.84,y=455)


welcomePage.mainloop()
