from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
from PIL import  ImageTk, Image, ImageFilter
import random
import os
import pymysql
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
def recommended_page_fn(gmail):
    
    RecommenedItemsPage = Tk()
    width, height = RecommenedItemsPage.winfo_screenwidth(), RecommenedItemsPage.winfo_screenheight()
    RecommenedItemsPage.geometry('%dx%d+0+0' % (width,height))
    RecommenedItemsPage.configure(background="#20b2aa")
    RecommenedItemsPage.title("Cash & Carry ")
    RecommenedItemsPage.resizable(False, False)
    RecommenedItemsPage.state('zoomed')

    p1 = PhotoImage(file = 'images/back.PNG')
# ---------------------- Setting icon of master window
    RecommenedItemsPage.iconphoto(False, p1)

    back_image = Image.open("images\\Trending.JPG")
    # resize the image and apply a high-quality down sampling filter
    back_image = back_image.resize((width,height), Image.Resampling.LANCZOS)
    back_image = back_image.filter(ImageFilter.GaussianBlur(1))
    # PhotoImage class is used to add image to widgets, icons etc
    back_image = ImageTk.PhotoImage(back_image)
    # create a label
    backimage = Label(RecommenedItemsPage, image = back_image, bg='#222A35')
    # set the image as img
    backimage.image = back_image
    backimage.place(height=height,width=width,x=0, y=0)



    # Cash_Label
    Font = ("Leelawadee",'36','bold')
    Cash_Label = Label(RecommenedItemsPage,bg='#20b2aa',bd=0,text='CASH',fg='white',font=Font)
    Cash_Label.place(x=760,y=208,height=55,width=470)
    # And_Label
    Font = ("Leelawadee",'36','bold')
    And_Label = Label(RecommenedItemsPage,bg='white',bd=0,text='&',fg='black',font=Font)
    And_Label.place(x=780,y=283,height=45,width=450)
    # Carry_Label
    Font = ("Leelawadee",'36','bold')
    Carry_Label = Label(RecommenedItemsPage,bg='#20b2aa',bd=0,text='CARRY',fg='white',font=Font)
    Carry_Label.place(x=760,y=338,height=55,width=470)


    # trending label
    Font = ("Leelawadee",'14','bold')
    Font_tuple = ("Brush Script MT", 30)
    trending_label = Label(RecommenedItemsPage,bg='#20b2aa',bd=0,text='Trending',fg='white',font= Font_tuple)
    trending_label.place(x=30,y=20,height=30,width=470)

    # IMAGES LABELS
   
    connection = pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
    cur = connection.cursor()
    cur.execute('select item_name from stock_product')
    quant = cur.fetchall()

    list_ = [list(quant),list(quant)]
    groc_data = pd.DataFrame(list_)


    #groc_data[len(groc_data.columns)] = ''

    #groc_data= pd.read_csv("Grocery_data.csv",header=None)

    items_data=groc_data.transpose()
    unique_items=[]

    for i in range(len(groc_data)):
        transaction=list(set(items_data[i]))
        [unique_items.append(x) for x in transaction if x not in unique_items]

    encoded_vals=[]
    # one hot encoding for supplying data in the apriori algorithm
    for i, rows in groc_data.iterrows():
        labels={}
        uncommons=list( set(unique_items)-set(rows))
        commons=list( set(unique_items).intersection(rows))

    for un in uncommons:
        labels[un] = 0

    for com in commons:
        labels[com] = 1
        encoded_vals.append(labels)

    encoded_data = pd.DataFrame(encoded_vals)
    print("\nOne hot encoded data:\n", encoded_data.head(10),"\n")

    frequent_items = apriori(encoded_data, min_support=0.0085, use_colnames=True)
    print(frequent_items["itemsets"])

    print(frequent_items.iloc[[0,1,2,3,4,5], [1]])

    print("Top 6 frequent items:\n",frequent_items.head(6),"\n")

    products_list = frequent_items.head(6)
    final_product_list = []
    allitems = products_list["itemsets"].tolist()
    sets=[allitems[0]]
    finalone = [list(x) for x in sets]
    final_product_list.append(finalone[0][0][0])
    sets=[allitems[1]]
    finalone = [list(x) for x in sets]
    final_product_list.append(finalone[0][0][0])
    sets=[allitems[2]]
    finalone = [list(x) for x in sets]
    final_product_list.append(finalone[0][0][0])
    sets=[allitems[3]]
    finalone = [list(x) for x in sets]
    final_product_list.append(finalone[0][0][0])
    sets=[allitems[4]]
    finalone = [list(x) for x in sets]
    final_product_list.append(finalone[0][0][0])
    sets=[allitems[5]]
    finalone = [list(x) for x in sets]
    final_product_list.append(finalone[0][0][0])


    print(final_product_list)
    cur.execute('select photo from stock_product where item_name=%s',final_product_list[0])
    data = cur.fetchall()   
    # opens the image
    image1 = Image.open(data[0][0])
    # resize the image and apply a high-quality down sampling filter
    image1 = image1.resize((140,80), Image.Resampling.LANCZOS)
    # PhotoImage class is used to add image to widgets, icons etc
    image1 = ImageTk.PhotoImage(image1)
    # create a label
    image1log = Label(RecommenedItemsPage, image = image1,bg='#ffffff')
    # set the image as img
    image1log.image = image1
    image1log.place(height=80,width=140,x=32, y=60)

    cur.execute('select photo from stock_product where item_name=%s',final_product_list[1])
    data = cur.fetchall()  
    # opens the image
    image2 = Image.open(data[0][0])
    # resize the image and apply a high-quality down sampling filter
    image2 = image2.resize((140,80), Image.Resampling.LANCZOS)
    # PhotoImage class is used to add image to widgets, icons etc
    image2 = ImageTk.PhotoImage(image2)
    # create a label
    image2log = Label(RecommenedItemsPage, image = image2,bg='#ffffff')
    # set the image as img
    image2log.image = image2
    image2log.place(height=80,width=140,x=200, y=60)

    cur.execute('select photo from stock_product where item_name=%s',final_product_list[2])
    data = cur.fetchall()  
    print(data)
    # opens the image
    image3 = Image.open(data[0][0])
    # resize the image and apply a high-quality down sampling filter
    image3 = image3.resize((140,80), Image.Resampling.LANCZOS)
    # PhotoImage class is used to add image to widgets, icons etc
    image3 = ImageTk.PhotoImage(image3)
    # create a label
    image3log = Label(RecommenedItemsPage, image = image3,bg='#ffffff')
    # set the image as img
    image3log.image = image3
    image3log.place(height=80,width=140,x=370, y=65)
    


    image1_label = Label(RecommenedItemsPage,bg='#20b2aa',bd=0, text=final_product_list[0])
    image1_label.place(x=30,y=165,height=30,width=150)

    image2_label = Label(RecommenedItemsPage,bg='#20b2aa',bd=0, text=final_product_list[1])
    image2_label.place(x=190,y=165,height=30,width=150)

    image3_label = Label(RecommenedItemsPage,bg='#20b2aa',bd=0, text=final_product_list[2])
    image3_label.place(x=350,y=165,height=30,width=150)

    cur.execute('select photo from stock_product where item_name=%s',final_product_list[3])
    data = cur.fetchall()  
    # opens the image
    image4 = Image.open(data[0][0])
    # resize the image and apply a high-quality down sampling filter
    image4 = image4.resize((140,80), Image.Resampling.LANCZOS)
    # PhotoImage class is used to add image to widgets, icons etc
    image4 = ImageTk.PhotoImage(image4)
    # create a label
    image4log = Label(RecommenedItemsPage, image = image4,bg='#ffffff')
    # set the image as img
    image4log.image = image4
    image4log.place(height=80,width=140,x=40, y=210)

    cur.execute('select photo from stock_product where item_name=%s',final_product_list[4])
    print(final_product_list)
    data = cur.fetchall()  
    # opens the image
    image5 = Image.open(data[0][0])
    # resize the image and apply a high-quality down sampling filter
    image5 = image5.resize((140,80), Image.Resampling.LANCZOS)
    # PhotoImage class is used to add image to widgets, icons etc
    image5 = ImageTk.PhotoImage(image5)
    # create a label
    image5log = Label(RecommenedItemsPage, image = image5,bg='#ffffff')
    # set the image as img
    image5log.image = image5
    image5log.place(height=80,width=140,x=203, y=210)

    cur.execute('select photo from stock_product where item_name=%s',final_product_list[5])
    data = cur.fetchall()  
    # opens the image
    image6 = Image.open(data[0][0])
    # resize the image and apply a high-quality down sampling filter
    image6 = image6.resize((140,80), Image.Resampling.LANCZOS)
    # PhotoImage class is used to add image to widgets, icons etc
    image6 = ImageTk.PhotoImage(image6)
    # create a label
    image6log = Label(RecommenedItemsPage, image = image6,bg='#ffffff')
    # set the image as img
    image6log.image = image6
    image6log.place(height=80,width=140,x=370, y=210)





    image4_label = Label(RecommenedItemsPage,bg='#20b2aa',bd=0,text=final_product_list[3])
    image4_label.place(x=30,y=315,height=30,width=150)

    image5_label = Label(RecommenedItemsPage,bg='#20b2aa',bd=0,text=final_product_list[4])
    image5_label.place(x=190,y=315,height=30,width=150)

    image6_label = Label(RecommenedItemsPage,bg='#20b2aa',bd=0,text=final_product_list[5])
    image6_label.place(x=350,y=315,height=30,width=150)

    # billing page button
    def billing_page_fun():
        from home import home_method
        RecommenedItemsPage.destroy()
        
        home_method(gmail)
        
    Font = ("Leelawadee",'13','bold')
    billing_page_button = Button(RecommenedItemsPage,text='Billing Page',bg='white',fg='black',font=Font,bd=0,command=billing_page_fun)
    billing_page_button.place(x=RecommenedItemsPage.winfo_screenwidth()/2 ,y=730,height=30,width=500,anchor='center')

    RecommenedItemsPage.mainloop()
