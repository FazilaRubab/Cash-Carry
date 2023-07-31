from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import os
import tkinter as tk
import tkinter
from datetime import datetime
from datetime import date
from PIL import  ImageTk, Image, ImageFilter

# ---------------------- page setting
empLoginPage = Tk()
width, height = empLoginPage.winfo_screenwidth(), empLoginPage.winfo_screenheight()
empLoginPage.geometry('%dx%d+0+0' % (width,height))
empLoginPage.configure(background="#20b2aa")
empLoginPage.title("Cash & Carry")
empLoginPage.resizable(False, False)


# ---------------------- ------------------set icon
icon = PhotoImage(file = 'images/back.PNG')
# ---------------------- Setting icon of master window
empLoginPage.iconphoto(False, icon)


back_image = Image.open("images\login_user.jpeg")
# resize the image and apply a high-quality down sampling filter
back_image = back_image.resize((width,height), Image.Resampling.LANCZOS)
back_image = back_image.filter(ImageFilter.GaussianBlur(1))
# PhotoImage class is used to add image to widgets, icons etc
back_image = ImageTk.PhotoImage(back_image)
# create a label
backimage = Label(empLoginPage, image = back_image, bg='#222A35')
# set the image as img
backimage.image = back_image
backimage.place(height=height,width=width,x=0, y=0)

Font_tuple = ("Brush Script MT", 30)

title1 = Label(empLoginPage, text="Log In", font= Font_tuple, bg="#000000", fg="#20b2aa").place(x=715, y=124)

email_label = Label(empLoginPage, text="Email Address", font="Leelawadee 13", bg="#000000" ,fg="#20b2aa").place(x= 560, y=219)
email_entry = Entry(empLoginPage, font="Leelawadee 13", bg= "black", fg= "white")
email_entry.place(x=556, y=254, width=354)


password_label = Label(empLoginPage, text="Password", font="Leelawadee 13", bg="#000000" ,fg="#20b2aa").place(x=559, y=285)
password_entry = Entry(empLoginPage, font="Leelawadee 13", bg= "black", fg= "white")
password_entry.place(x=558, y=321, width=351)


#functions
def login():
    gmail = email_entry.get()
    if email_entry.get()=="" or password_entry.get()=="":
            messagebox.showerror("Error!","All fields are required",parent=empLoginPage)
    else:
        try:
            connection=pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
            cur = connection.cursor()
            cur.execute("select * from user_register where email=%s and password=%s",(email_entry.get(),password_entry.get()))
            row=cur.fetchone()
            if row == None:
                messagebox.showerror("Error!","Invalid USERNAME & PASSWORD",parent=empLoginPage)
            else:
                messagebox.showinfo("Success","Welcome to the Cash & Carry",parent=empLoginPage)
                # Clear all the entries
        
                empLoginPage.destroy()
                #from home import home_method
                #home_method(gmail)
                from recomendPage import recommended_page_fn
                recommended_page_fn(gmail)
                email_entry.delete(0,END)
                password_entry.delete(0,END)
                
                connection.close()

        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=empLoginPage)
    

def signup():
    empLoginPage.withdraw()
    os.system("python empSignUp.py")
    empLoginPage.deiconify()



login_button = Button(empLoginPage, text= "Login", command=login, font="Leelawadee 14", bd=0,
                    cursor="hand2", bg="#20b2aa", fg="white").place(x=722, y=406, width=150)

create_button = Button(empLoginPage, text="Create New Account", command=signup,
                            font="Leelawadee 14", bd=0,
                            cursor="hand2", bg="#000000", fg="#20b2aa").place(x=684, y=475, width=200)


forget_button = Button(empLoginPage, text="Forget Password", command=signup,
                            font="Leelawadee 14", bd=0,
                            cursor="hand2", bg="#000000", fg="#20b2aa").place(x=695, y=528, width=185)

empLoginPage.mainloop()