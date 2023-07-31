import pymysql
import mysql.connector
import re
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import filedialog
from tkinter import scrolledtext as tkst
from PIL import  ImageTk, Image, ImageFilter

global filename
filename=''
global binarydata
binarydata = ''

# ---------------------- page setting
admHomePage = Tk()
width, height = admHomePage.winfo_screenwidth(), admHomePage.winfo_screenheight()
admHomePage.geometry('%dx%d+0+0' % (width,height))
admHomePage.configure(background="#222A35")
admHomePage.title("Cash & Carry")
admHomePage.resizable(False, False)
admHomePage.state('zoomed')


# ---------------------- ------------------set icon
p1 = PhotoImage(file = 'images/back.PNG')
# ---------------------- Setting icon of master window
admHomePage.iconphoto(False, p1)

# ======================================= Back Ground image ================
img5 = Image.open("images\\admin_dashboard.png")
# resize the image and apply a high-quality down sampling filter
img5 = img5.resize((width,height), Image.Resampling.LANCZOS)
# PhotoImage class is used to add image to widgets, icons etc
img5 = ImageTk.PhotoImage(img5)
# create a label
admin_manual_logo = Label(admHomePage, image = img5, bg='#222A35')
# set the image as img
admin_manual_logo.image = img5
admin_manual_logo.place(height=height,width=width,x=0, y=0)

categorybox= ttk.Combobox(admHomePage, text="drop down",font="Leelawadee 13",state='readonly')
categorybox['values']=("Select","Footwear","Clothes","Cosmetics","Bags","Appliances","Electronics","Jewlery")
categorybox.place(x=55, y=height/4.1, width=350,height=25)
categorybox.current(0)

item_name = Entry(admHomePage,font=("arial"),bg='deep sky blue3',bd=0,fg='white')
item_name.place(x=55, y=height/2.7, width=350,height=25)

price = Entry(admHomePage,font=("arial"),bg='deep sky blue3',bd=0,fg='white')
price.place(x=55, y=height/2.01, width=350,height=25)

quantity = Entry(admHomePage,font=("arial"),bg='deep sky blue3',bd=0,fg='white')
quantity.place(x=55, y=height/1.6, width=350,height=25)

bill_id_search = Entry(admHomePage,font=("arial"),bg='deep sky blue3',bd=0,fg='white')
bill_id_search.place(x=width/2.1, y=height/1.13, width=300,height=25)

# =============================================  TREE VIEW TO SHOW DATA ===============================
# ---------- Using treeview widget ------------
treev = ttk.Treeview(admHomePage, selectmode ='browse')
#  ------------ Calling pack method w.r.to treeview ------------
treev.place(height=550,width=width/1.6, x=width/2.9,y=height/14)

#  ------------ Defining number of columns ------------
treev["columns"] = ("1", "2", "3","4","5")

# Defining heading
treev['show'] = 'headings'
#  ------------ Assigning the width and anchor to the
# respective columns ------------
treev.column("1", width = 100, anchor ='c')
treev.column("2", width = 100, anchor ='c')
treev.column("3", width = 100, anchor ='c')
treev.column("4", width = 100, anchor ='c')
treev.column("5", width = 100, anchor ='c')

treev.heading("1", text ="Sr. No")
treev.heading("2", text ="Category")
treev.heading("3", text ="Item Name")
treev.heading("4", text ="Price")
treev.heading("5", text ="Quantity")

treev.delete(*treev.get_children())
connection = pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
cur = connection.cursor()
cur.execute("""SELECT * FROM stock_product;""")
data_2 = cur.fetchall()
# ---------- INSERT ALL VALUES ITNO TREEVIEW FROM DATABASE -----------
indexer = 1
for value in data_2:
    treev.insert("", 'end', text ="L"+str(indexer),values =(value[0],value[1],value[2],value[3],value[4]))
    indexer +=1
connection.close()


# ======================================= fuctions ========================
def openfilename():
    global filename
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(title ="Select Single Image", filetypes =(("PNG", "*.png"),("JPG", "*.jpg")))
    name = filename.split('/')[-1]
    img10 = Image.open(filename.replace('/','//'))
    img10.save('products/{}'.format(name),quality=200)
    filename = 'products/{}'.format(name)
    return filename

def add():
    global filename
    if categorybox.get()=='Select':
        messagebox.showerror("Failed","Please Select Category",parent=admHomePage)
    elif item_name.get()=='' or price.get()=='' or quantity.get()=='':
        messagebox.showerror("Failed","No Field Remains Empty",parent=admHomePage)
    elif filename=='':
        messagebox.showerror("Failed","Plase select image of product",parent=admHomePage)    
    else:
        connection = pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
        cur = connection.cursor()
        query = "select item_name from stock_product where item_name=%s"
        cur.execute(query,(item_name.get()))
        row=cur.fetchone()
        if row!=None:
            messagebox.showerror("Failed","Item Already available. Please Update Product",parent=admHomePage)
        else:
            try:
                
                cur.execute("insert into stock_product (category,item_name,price,quantity,photo) values(%s,%s,%s,%s,%s)",
                                (
                                    categorybox.get(),
                                    item_name.get(),
                                    price.get(),
                                    quantity.get(),
                                    filename
                                ))
                connection.commit()
                
                messagebox.showinfo("Success","Item Added Successfully",parent=admHomePage)
                treev.delete(*treev.get_children())
                categorybox.current(0)
                item_name.delete(0,END)
                price.delete(0,END)
                quantity.delete(0,END)
                cur.execute("""SELECT * FROM stock_product;""")
                data_2 = cur.fetchall()
                # ---------- INSERT ALL VALUES ITNO TREEVIEW FROM DATABASE -----------
                indexer = 1
                for value in data_2:
                    treev.insert("", 'end', text ="L"+str(indexer),values =(value[0],value[1],value[2],value[3],value[4]))
                    indexer +=1
                connection.close()
            except Exception as es:
                messagebox.showerror("Error",f"Error Due To:  {str(es)}",parent=admHomePage)
def update():
    connection = pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
    cur = connection.cursor()
    if categorybox.get()=='Select':
        messagebox.showerror("Failed","Please Select Category",parent=admHomePage)
    elif item_name.get()=='' or price.get()=='' or quantity.get()=='':
        messagebox.showerror("Failed","No Field Remains Empty",parent=admHomePage)
    else:
        query = "select item_name from stock_product where item_name=%s"
        cur.execute(query,(item_name.get()))
        row=cur.fetchone()
        if row!=None:
            try:
                cur.execute("update stock_product set category=%s,price=%s,quantity=%s where item_name=%s",
                                (   categorybox.get(),
                                    price.get(),
                                    quantity.get(),
                                    item_name.get()
                                ))
                connection.commit()
                
                messagebox.showinfo("Success","Item Updated Successfully",parent=admHomePage)
                treev.delete(*treev.get_children())
                categorybox.current(0)
                item_name.delete(0,END)
                price.delete(0,END)
                quantity.delete(0,END)
                cur.execute("""SELECT * FROM stock_product;""")
                data_2 = cur.fetchall()
                # ---------- INSERT ALL VALUES ITNO TREEVIEW FROM DATABASE -----------
                indexer = 1
                for value in data_2:
                    treev.insert("", 'end', text ="L"+str(indexer),values =(value[0],value[1],value[2],value[3],value[4]))
                    indexer +=1
                connection.close()
            except Exception as es:
                messagebox.showerror("Error",f"Error Due To:  {str(es)}",parent=admHomePage)
        else:
            messagebox.showerror("Failed","Item not Found. Please Add product",parent=admHomePage)
        
def delete():
    connection = pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
    cur = connection.cursor()
    if item_name.get()=='':
        messagebox.showerror("Failed","Enter Item Name You want to Delete",parent=admHomePage)
    else:
        query = "select item_name from stock_product where item_name=%s"
        cur.execute(query,(item_name.get()))
        row=cur.fetchone()
        if row!=None:
            try:
                cur.execute("delete from stock_product where item_name=%s",(item_name.get()))
                connection.commit()
                
                messagebox.showinfo("Success","Item Deleted **_**",parent=admHomePage)
                treev.delete(*treev.get_children())
                categorybox.current(0)
                item_name.delete(0,END)
                price.delete(0,END)
                quantity.delete(0,END)
                cur.execute("""SELECT * FROM stock_product;""")
                data_2 = cur.fetchall()
                # ---------- INSERT ALL VALUES ITNO TREEVIEW FROM DATABASE -----------
                indexer = 1
                for value in data_2:
                    treev.insert("", 'end', text ="L"+str(indexer),values =(value[0],value[1],value[2],value[3],value[4]))
                    indexer +=1
                connection.close()
            except Exception as es:
                messagebox.showerror("Error",f"Error Due To:  {str(es)}",parent=admHomePage)
        else:
            messagebox.showerror("Failed","Item not Found. Please select availble item",parent=admHomePage)
    
def search():
    if bill_id_search=='':
        messagebox.showerror("Error",'Enter Your bill id for Search',parent=admHomePage)
    else:
        dataview = Toplevel()
        width, height = dataview.winfo_screenwidth(), dataview.winfo_screenheight()
        dataview.geometry('%dx%d+0+0' % (width,height))
        dataview.configure(background="#00ccd3")
        dataview.title("Cash & Carry")
        dataview.resizable(False, False)
        dataview.grab_set()
        
        # =============================================  TREE VIEW TO SHOW DATA ===============================
        # ---------- Using treeview widget ------------
        treev = ttk.Treeview(dataview, selectmode ='browse')
        #  ------------ Calling pack method w.r.to treeview ------------
        treev.place(height=550,width=width, x=0,y=height/14)

        #  ------------ Defining number of columns ------------
        treev["columns"] = ("1", "2", "3","4","5")

        # Defining heading
        treev['show'] = 'headings'
        #  ------------ Assigning the width and anchor to the
        # respective columns ------------
        treev.column("1", width = 250, anchor ='c')
        treev.column("2", width = 250, anchor ='c')
        treev.column("3", width = 250, anchor ='c')
        treev.column("4", width = 250, anchor ='c')
        treev.column("5", width = 250, anchor ='c')

        treev.heading("1", text ="Serial No")
        treev.heading("2", text ="Bill Id")
        treev.heading("3", text ="User Name")
        treev.heading("4", text ="Item Name")
        treev.heading("5", text ="Price")

        
        
        treev.delete(*treev.get_children())
        connection = pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
        cur = connection.cursor()
        cur.execute("SELECT * FROM bill_data where bill_id=%s",bill_id_search.get())
        data_2 = cur.fetchall()
        # ---------- INSERT ALL VALUES ITNO TREEVIEW FROM DATABASE -----------
        indexer = 1
        for value in data_2:
            treev.insert("", 'end', text ="L"+str(indexer),values =(value[0],value[1],value[2],value[3],value[4]))
            indexer +=1
        connection.close()
def bill_history():
    dataview = Toplevel()
    width, height = dataview.winfo_screenwidth(), dataview.winfo_screenheight()
    dataview.geometry('%dx%d+0+0' % (width,height))
    dataview.configure(background="#00ccd3")
    dataview.title("Cash & Carry")
    dataview.resizable(False, False)
    dataview.grab_set()
    
    # =============================================  TREE VIEW TO SHOW DATA ===============================
    # ---------- Using treeview widget ------------
    treev = ttk.Treeview(dataview, selectmode ='browse')
    #  ------------ Calling pack method w.r.to treeview ------------
    treev.place(height=550,width=width, x=0,y=height/14)

    #  ------------ Defining number of columns ------------
    treev["columns"] = ("1", "2", "3","4","5")

    # Defining heading
    treev['show'] = 'headings'
    #  ------------ Assigning the width and anchor to the
    # respective columns ------------
    treev.column("1", width = 250, anchor ='c')
    treev.column("2", width = 250, anchor ='c')
    treev.column("3", width = 250, anchor ='c')
    treev.column("4", width = 250, anchor ='c')
    treev.column("5", width = 250, anchor ='c')

    treev.heading("1", text ="Serial No")
    treev.heading("2", text ="Bill Id")
    treev.heading("3", text ="User Name")
    treev.heading("4", text ="Item Name")
    treev.heading("5", text ="Price")
    treev.delete(*treev.get_children())
    connection = pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
    cur = connection.cursor()
    cur.execute("SELECT * FROM bill_data")
    data_2 = cur.fetchall()
    # ---------- INSERT ALL VALUES ITNO TREEVIEW FROM DATABASE -----------
    indexer = 1
    for value in data_2:
        treev.insert("", 'end', text ="L"+str(indexer),values =(value[0],value[1],value[2],value[3],value[4]))
        indexer +=1
    connection.close()
# # ========================== BUTTONS FOR ADD UPDATE, DELTE AND CLEAR ALL

addphoto_btn= Button(admHomePage,text="upload image", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=openfilename,bd=0)
addphoto_btn.place(x=90, y=height/6.43, width=width/10,height=35)

add_btn= Button(admHomePage,text="Add", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=add,bd=0)
add_btn.place(x=90, y=height/1.42, width=width/5,height=38)

update_btn= Button(admHomePage,text="Update", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=update,bd=0)
update_btn.place(x=90, y=height/1.27, width=width/5,height=38)

delete_btn= Button(admHomePage,text="Delete", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=delete,bd=0)
delete_btn.place(x=90, y=height/1.15, width=width/5,height=38)

search_btn= Button(admHomePage,text="Search", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=search,bd=0)
search_btn.place(x=width/1.4, y=height/1.13, width=width/12,height=35)

bill_his_btn= Button(admHomePage,text="Bill History", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=bill_history,bd=0)
bill_his_btn.place(x=width/1.2, y=height/1.13, width=width/9,height=35)


admHomePage.mainloop()