from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pymysql
import os
import tkinter as tk
import tkinter
from datetime import datetime
from datetime import date
from PIL import  ImageTk, Image, ImageFilter

# ---------------------- page setting
admLoginPage = Tk()
width, height = admLoginPage.winfo_screenwidth(), admLoginPage.winfo_screenheight()
admLoginPage.geometry('%dx%d+0+0' % (width,height))
admLoginPage.configure(background="#20b2aa")
admLoginPage.title("Cash & Carry")
admLoginPage.resizable(False, False)


# ---------------------- ------------------set icon
p1 = PhotoImage(file = 'images/back.PNG')
# ---------------------- Setting icon of master window
admLoginPage.iconphoto(False, p1)

img5 = Image.open("images\\admin_login.JPG")
# resize the image and apply a high-quality down sampling filter
img5 = img5.resize((width,height), Image.Resampling.LANCZOS)
img5 = img5.filter(ImageFilter.GaussianBlur(1))
# PhotoImage class is used to add image to widgets, icons etc
img5 = ImageTk.PhotoImage(img5)
# create a label
admin_manual_logo = Label(admLoginPage, image = img5, bg='#222A35')
# set the image as img
admin_manual_logo.image = img5
admin_manual_logo.place(height=height,width=width,x=0, y=0)




Font_tuple = ("Brush Script MT", 30)

title1 = Label(admLoginPage, text="Log In (Admin)", font= Font_tuple, bg="#000000" ,fg="#20b2aa").place(x=665, y=120)

email_label = Label(admLoginPage, text="Email Address", font="Leelawadee 13", bg="#000000" ,fg="#20b2aa").place(x=560, y=219)
email_entry = Entry(admLoginPage, font="Leelawadee 13", bg= "black", fg= "white")
email_entry.place(x=556, y=250, width=354)

password_label = Label(admLoginPage, text="New password", font="Leelawadee 13", bg="#000000" ,fg="#20b2aa").place(x=543, y=283,width=135)

password_entry = Entry(admLoginPage, font="Leelawadee 13", bg= "black", fg= "white")
password_entry.place(x=558, y=316, width=351)

#functions
def login():
    if email_entry.get()=="" or password_entry.get()=="":
            messagebox.showerror("Error!","All fields are required",parent=admLoginPage)
    else:
        try:
            connection=pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
            cur = connection.cursor()
            cur.execute("select * from admin_register where email=%s and password=%s",(email_entry.get(),password_entry.get()))
            row=cur.fetchone()
            if row == None:
                messagebox.showerror("Error!","Invalid USERNAME & PASSWORD",parent=admLoginPage)
            else:
                messagebox.showinfo("Success","Welcome to the Cash & Carry",parent=admLoginPage)
                # Clear all the entries
                email_entry.delete(0,END)
                password_entry.delete(0,END)
                
                admLoginPage.withdraw()
                os.system("python adm_home.py")
                admLoginPage.deiconify()
                
                connection.close()

        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=admLoginPage)

login_button = Button(admLoginPage, text="Log In",command=login, font="Leelawadee 14", bd=0,
                    cursor="hand2", bg="#20b2aa", fg="white").place(x=722, y=400, width=150)



admLoginPage.mainloop()

