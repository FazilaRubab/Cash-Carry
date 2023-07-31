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
empSignUpPage = Tk()
width, height = empSignUpPage.winfo_screenwidth(), empSignUpPage.winfo_screenheight()
empSignUpPage.geometry('%dx%d+0+0' % (width,height))
empSignUpPage.configure(background="#20b2aa")
empSignUpPage.title("Cash & Carry")
empSignUpPage.resizable(False, False)


# ---------------------- ------------------set icon
p1 = PhotoImage(file = 'images/back.PNG')
# ---------------------- Setting icon of master window
empSignUpPage.iconphoto(False, p1)

img5 = Image.open("images\\sign_up.JPG")
# resize the image and apply a high-quality down sampling filter
img5 = img5.resize((width,height), Image.Resampling.LANCZOS)
img5 = img5.filter(ImageFilter.GaussianBlur(1))
# PhotoImage class is used to add image to widgets, icons etc
img5 = ImageTk.PhotoImage(img5)
# create a label
admin_manual_logo = Label(empSignUpPage, image = img5, bg='#222A35')
# set the image as img
admin_manual_logo.image = img5
admin_manual_logo.place(height=height,width=width,x=0, y=0)



Font_tuple = ("Brush Script MT", 25)


title1 = Label(empSignUpPage, text="Sign Up", font= Font_tuple ,bg="#000000", fg="#20b2aa").place(x=715, y=125)
title2 = Label(empSignUpPage, text="Join with us", font="Leelawadee 13",bg="#000000", fg="#20b2aa").place(x=738, y=165)

f_name = Label(empSignUpPage, text="First name", font="Leelawadee 13",bg="#000000", fg="#20b2aa").place(x=559, y=223)
l_name = Label(empSignUpPage, text="Last name", font="Leelawadee 13",bg="#000000", fg="#20b2aa").place(x=790, y=223)

fname_txt = Entry(empSignUpPage,font="Leelawadee 13", background="black", fg="white")
fname_txt.place(x=558, y=251, width=207)

lname_txt = Entry(empSignUpPage, font="Leelawadee 13", background="black", fg="white")
lname_txt.place(x=789, y=251, width=207)

email = Label(empSignUpPage, text="Email", font="Leelawadee 13", bg="#000000", fg="#20b2aa").place(x=556, y=304)

email_txt = Entry(empSignUpPage,font="Leelawadee 13", background="black", fg="white")
email_txt.place(x=556, y=337, width=440)

sec_question = Label(empSignUpPage, text="Security questions", font="Leelawadee 13",bg="#000000", fg="#20b2aa").place(x=541, y=389, width=170)
answer = Label(empSignUpPage, text="Answer", font="Leelawadee 13" , bg="#000000", fg="#20b2aa" ).place(x=787, y=389)

questions = ttk.Combobox(empSignUpPage,font="Leelawadee 13",state='readonly',justify=CENTER )
questions['values'] = ("Select","What's your pet name?","Your first teacher name","Your birthplace", "Your favorite movie")
questions.place(x=558,y=423,width=208)
questions.current(0)

answer_txt = Entry(empSignUpPage,font="Leelawadee 13", background="black", fg="white")
answer_txt.place(x=788, y=422, width=204)



password =  Label(empSignUpPage, text="New password", font="Leelawadee 13",bg="#000000",fg="#20b2aa").place(x=531, y=473,width=170)

password_txt = Entry(empSignUpPage,font="Leelawadee 13", background="black", fg="white")
password_txt.place(x=554, y=508, width=440)

terms = IntVar()
terms_and_con = Checkbutton(empSignUpPage,text="I Agree The Terms & Conditions",variable=terms,onvalue=1,offvalue=0,bg="#000000", fg="#20b2aa", font=("times new roman",12)).place(x=561,y=558)



#functions
def signup_func():
    if fname_txt.get()=="" or lname_txt.get()=="" or email_txt.get()=="" or questions.get()=="Select" or answer_txt.get()=="" or password_txt.get() == "":
        messagebox.showerror("Error!","Sorry!, All fields are required",parent=empSignUpPage)

    elif terms.get() == 0:
        messagebox.showerror("Error!","Please Agree with our Terms & Conditions",parent=empSignUpPage)

    else:
        try:
            connection = pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
            cur = connection.cursor()
            cur.execute("select * from user_register where email=%s",email_txt.get())
            row=cur.fetchone()

            # Check if th entered email id is already exists or not.
            if row!=None:
                messagebox.showerror("Error!","The email id is already exists, please try again with another email id",parent=empSignUpPage)
            else:
                cur.execute("insert into user_register (f_name,l_name,email,question,answer,password) values(%s,%s,%s,%s,%s,%s)",
                                (
                                    fname_txt.get(),
                                    lname_txt.get(),
                                    email_txt.get(),
                                    questions.get(),
                                    answer_txt.get(),
                                    password_txt.get()
                                ))
                connection.commit()
                connection.close()
                messagebox.showinfo("Congratulations!","Register Successful",parent=empSignUpPage)
                fname_txt.delete(0,END)
                lname_txt.delete(0,END)
                email_txt.delete(0,END)
                answer_txt.delete(0,END)
                password_txt.delete(0,END)
        except Exception as es:
            messagebox.showerror("Error!",f"Error due to {es}",parent=empSignUpPage)
    

signup = Button(empSignUpPage,text="Sign Up",command=signup_func,font="Leelawadee 14",bd=0,cursor="hand2",bg="#20b2aa",fg="white").place(x=660,y=617,width=250)



empSignUpPage.mainloop()