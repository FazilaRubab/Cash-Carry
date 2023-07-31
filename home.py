import pymysql
import re
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
from PIL import  ImageTk, Image, ImageFilter
import random
import os


def home_method(gmail):

    connection = pymysql.connect(host="localhost", user="root", password="saqib32", database="Billing")
    cur = connection.cursor()

    # ---------------------- page setting
    empHomePage = Tk()
    width, height = empHomePage.winfo_screenwidth(), empHomePage.winfo_screenheight()
    empHomePage.geometry('%dx%d+0+0' % (width,height))
    empHomePage.configure(background="#222A35")
    empHomePage.title("Cash & Carry")
    empHomePage.resizable(False, False)
    empHomePage.state('zoomed')


    # ---------------------- ------------------set icon
    p1 = PhotoImage(file = 'images/back.PNG')
    # ---------------------- Setting icon of master window
    empHomePage.iconphoto(False, p1)

    # ======================================= Back Ground image ================
    img5 = Image.open("images\\add_to_cart_page.png")
    # resize the image and apply a high-quality down sampling filter
    img5 = img5.resize((width,height), Image.Resampling.LANCZOS)
    # PhotoImage class is used to add image to widgets, icons etc
    img5 = ImageTk.PhotoImage(img5)
    # create a label
    admin_manual_logo = Label(empHomePage, image = img5, bg='#20b2aa')
    # set the image as img
    admin_manual_logo.image = img5

    admin_manual_logo.place(height=height,width=width,x=0, y=0)

    searchdata = Entry(empHomePage,font=("arial"),bg='#00A79D',bd=0)
    searchdata.place(x=500, y=60, width=width/2.88,height=25)

    categ= ttk.Combobox(empHomePage, text="drop down",font="Leelawadee 13",state='readonly')
    categ['values']=("Select","Footwear","Clothes","Cosmetics","Bags","Appliances","Electronics","Jewlery")
    categ.place(height=30,width=350,x=40, y=width/4.4)
    categ.current(0)

    connection = pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
    cur = connection.cursor()

    #================================= Product Database ComboBox ==================
    cur.execute('select item_name from stock_product;')
    data = cur.fetchall()
    item_names = []
    item_names.append('select')
    for i in data:
        item_names.append(i[0])
    itemsbox= ttk.Combobox(empHomePage, text="drop down1",font="Leelawadee 13",state='readonly')
    itemsbox['values']=item_names
    itemsbox.place(height=30,width=350,x=40, y=width/3.36)
    itemsbox.current(0)

    quantity = Entry(empHomePage,font=("arial"),bg='#00A79D',bd=0)
    quantity.place(x=40, y=width/2.68, width=350,height=25)

    billarea = Text(empHomePage)
    billarea.place(height=470,width=470, x=width/1.6,y=height/4)


    def billdata(data):
        billarea.insert(END,"Welcome to Cash & Carry\n")
        billarea.insert(END,"User Name: {} \n".format(data))
        billarea.insert(END,"#########################################################\n")
        billarea.insert(END,"Product\t\t\tQuantity\t\t\tPrice\n")
        billarea.insert(END,"#########################################################\n")
    cur.execute('select * from user_register where email =%s',gmail)
    data = cur.fetchone()
    billdata(data[0])
    # opens the image
    products_img = Image.open("images\\add_pic.png")
    # resize the image and apply a high-quality down sampling filter
    products_img = products_img.resize((200,300), Image.Resampling.LANCZOS)
    # PhotoImage class is used to add image to widgets, icons etc
    products_img = ImageTk.PhotoImage(products_img)
    # create a label
    prodoctlog = Label(empHomePage, image = products_img,bg='#ffffff')
    # set the image as img
    prodoctlog.image = products_img
    prodoctlog.place(height=400,width=300,x=590, y=240)

    prices = []
    iteM = []
    quanTity = []
    #----------------------------------------------ADD DATA BUTTON --------------------------------
    def add_to_cart_fun():
        

        #================================= Product Database ComboBox ==================
        category = categ.get()
        item_name = itemsbox.get()
        quantity_ = quantity.get()
        
        if quantity_ == '':
            messagebox.showerror("Error",'Must enter Quantity',parent=empHomePage)
        elif item_name == 'select' or category == 'select':
            messagebox.showerror("Error",'Please select Category with item',parent=empHomePage)
        else:
            cur.execute('select quantity from stock_product where item_name=%s',item_name)
            data = cur.fetchall()
            num = int(data[0][0])
            rem_quantity = num
            if rem_quantity<int(quantity_):
                messagebox.showerror("Error",'Not Enough Quantity Available',parent=empHomePage)
            else:
                rem_quantity = rem_quantity-int(quantity_)
                cur.execute('select photo from stock_product where item_name=%s',item_name)
                data = cur.fetchall()   
                # opens the image
                products_img = Image.open(data[0][0])
                # resize the image and apply a high-quality down sampling filter
                products_img = products_img.resize((200,300), Image.Resampling.LANCZOS)
                # PhotoImage class is used to add image to widgets, icons etc
                products_img = ImageTk.PhotoImage(products_img)
                # create a label
                prodoctlog = Label(empHomePage, image = products_img,bg='#ffffff')
                # set the image as img
                prodoctlog.image = products_img
                prodoctlog.place(height=400,width=300,x=590, y=240)
                
                
                cur.execute('select price from stock_product where item_name =%s',item_name)
                data = cur.fetchone()
                actual_price = int(data[0])
                total_price = int(quantity_)*actual_price
                prices.append(total_price)
                billarea.insert(END,'\n'+str(item_name)+'\t\t\t'+str(quantity_)+'\t\t\t'+str(int(quantity_)*actual_price))
                quanTity.append(quantity_)  
                print(quanTity)
                iteM.append(item_name)  
                cur.execute('update stock_product set quantity =%s where item_name=%s',(quantity_,item_name))
                connection.commit()
                            
        
    add_cart_btn= Button(empHomePage,text="Add To Cart", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=add_to_cart_fun,bd=0)
    add_cart_btn.place(x=83, y=width/2.28, width=width/5,height=35)

    def save_bill_fn():
        idbill = random.randint(300,50000)
        Total = sum(prices)
        billarea.insert(END,"\n#########################################################\n")
        billarea.insert(END,'Total Bill : {}'.format(Total))
        cur.execute('select f_name from user_register where email=%s',gmail)
        name = cur.fetchone()
        for i in range(len(prices)):
            cur.execute('insert into bill_data(bill_id,user_name,item_name,price,quantity)values(%s,%s,%s,%s,%s)',(str(idbill),
                name,
                iteM[i],
                prices[i],
                quanTity[i]
            ))
            #cur.execute('update stock_product set quantity =%s where item_name=%s',quanTity[i],iteM[i])
            connection.commit()
        for j in range(len(quanTity)):
            cur.execute('select quantity from stock_product where item_name =%s',iteM[j])
            data = cur.fetchone()
            print(data)
            quanTity[j]
            cur.execute('update stock_product set quantity =%s where item_name=%s',(quanTity[j],iteM[j]))
            connection.commit()
        
        messagebox.showinfo("Success",'Bill Saved Successfully, your id no is {}'.format(idbill),parent=empHomePage)
        
        
        
    save_bill_btn= Button(empHomePage,text="Save Bills", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=save_bill_fn,bd=0)
    save_bill_btn.place(x=width/1.3, y=height/1.09, width=width/11,height=37)

    def clear():
        billarea.delete('1.0',END)
        billdata(data[0])
    clr_cart_btn= Button(empHomePage,text="Clear", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=clear,bd=0)
    clr_cart_btn.place(x=width/1.129, y=height/1.09, width=width/11,height=37)

    def search():
        if searchdata=='':
            messagebox.showerror("Error",'Enter Your bill id for Search',parent=empHomePage)
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
            cur.execute("SELECT * FROM bill_data where bill_id=%s",searchdata.get())
            data_2 = cur.fetchall()
            # ---------- INSERT ALL VALUES ITNO TREEVIEW FROM DATABASE -----------
            indexer = 1
            for value in data_2:
                treev.insert("", 'end', text ="L"+str(indexer),values =(value[0],value[1],value[2],value[3],value[4]))
                indexer +=1
            connection.close()
            
        
    search_btn= Button(empHomePage,text="Search", bg="black",fg='white',font="Leelawadee 14",activebackground='black', command=search,bd=0)
    search_btn.place(x=width/1.44, y=height/17, width=width/11,height=35)
    
    def back():
        empHomePage.destroy()
        os.system("python welcome_page.py")
    clr_cart_btn= Button(empHomePage,text="Back", bg="black",fg='white',font="Leelawadee 17",activebackground='black', command=back,bd=0)
    clr_cart_btn.place(x=width/1.68, y=height/1.09, width=width/6.5,height=37)

    empHomePage.mainloop()