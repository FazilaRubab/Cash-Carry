import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pymysql

#taking data from database and take recommended items from data

connection=pymysql.connect(host="localhost", user="root", password= "saqib32", database="Billing")
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