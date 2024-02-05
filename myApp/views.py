from django.contrib import messages
import mysql.connector as ms
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
# from .models import graphEnquiry
import matplotlib
import matplotlib.pyplot as plt
from shutil import copy2
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
import matplotlib.style as style
matplotlib.use('Agg')
# style.use('dark_background')


def make_connection():
    mydb = ms.connect(
        host= "localhost",
        user= "root",
        password= "Vilas@343",
        database= "mart_sales"
    )
    return mydb

def base(request):
    return render(request, "base.html")

def home(request):
    return render(request, 'home.html')

def Analysis(request):
    return render(request, "Analysis.html")

def log_out(request):
    return redirect("/")

def feedback(request):
    return render(request, "Feedback.html")



username = ''
password = ''
def login_action(request):
    global username, password

    db_user = ''
    db_pass = ''
    mydb = make_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT*FROM login")
    login_cred = mycursor.fetchall()
     
    ds = request.POST
    for key, value in ds.items():
        if key == 'username':
            username = value
        if key == 'password':
            password = value

    for x in login_cred:
        db_user = x[0]
        db_pass = x[1]
        if db_user == username and db_pass == password:
            return redirect('/preference/')
    
    messages.info(request, 'INVALID CREDENTIALS !!!!')
    return redirect('/')



# ************************ Preference Form ***********************

def preference(request):
    if request.method == 'POST':
        preference = request.POST.get('prefrence')
        print(preference)
        if preference == "store_analysis":
            return redirect('store_analysis')
        elif preference == "product_analysis":
            return redirect('product_analysis')
        elif preference == None: 
            messages.info(request, 'Please Select Option...!')
            return redirect('/preference/')
            
    else: 
            return render(request,'prefrence_form.html')


# ********************* Get Column Function *****************************
def get_column_name(my_list1, uploadedFile):
    # sales = pd.read_csv('C:/Users/Vilas/Desktop/Train-Set.csv')
    # matching x_axis and y_axis value with column
    column_names = uploadedFile.columns.to_list()
    my_list = [None] * 20

    for item in column_names: 
        if 'year' in item.lower() and 'establishment' in item.lower(): 
            my_list[0] = item 
            
        if 'outlet' in item.lower() and 'type' in item.lower(): 
            my_list[1] = item 
        
        if 'stores' in item.lower() and 'markets' in item.lower(): 
            my_list[2] = item 

        if 'product' in item.lower() or 'inlet' in item.lower() or 'item' in item.lower() and 'type' in item.lower(): 
            my_list[3] = item 

        if 'outlet' in item.lower() and 'type' in item.lower(): 
            my_list[4] = item 

        if 'sales' in item.lower():
            my_list[5] = item

        if 'visibility' in item.lower():
            my_list[6] = item

        if 'location' in item.lower():
            my_list[7] = item
    
    return my_list



# **************************** Store Analysis Graphs ***********************************************
def locationWiseSalesOfTheStores(preference, my_list, uploadedFile): 
    # sales = pd.read_csv('C:/Users/Vilas/Desktop/Train-Set.csv')
    # matching x_axis and y_axis value with column
    column_name = uploadedFile.columns.tolist()
    my_list1 = get_column_name(my_list, uploadedFile)
    establishment_year = my_list1[0]
    outlet_type = my_list1[4]
    outlet_sales = my_list1[5]
    location_type = my_list1[7]
    

    if outlet_sales == None or outlet_type == None or location_type == None or establishment_year == None: 
        my_list[4] = f'the column you have entered does not exist' 
        my_list1[5] = f'thats why we cannot proceed your request'
    
    else: 
        sales_data = uploadedFile.sort_values(by=establishment_year, ascending=False) # move this line up
        store_names = sales_data[outlet_type].unique()
        for store_name in store_names:
            if preference.lower() in store_name.lower():
                preference = store_name 
                break
    
    
        #  we have store_name, x_quantity and y_quantity
        # now we will ask the user upto which row he wants to analyse data.
        fileName = "" 
        # Get the unique store names from the sales data
        store_names = sales_data[outlet_type].unique()
        fig,ax = plt.subplots()
        # Find the store type that matches the user input
        # Get the data for the selected store type
        interest_data = sales_data[sales_data[outlet_type] == preference]

        # Get the unique values in the x_column and sort theminterest_data = sales_data[sales_data['OutletType'] == user_interest]
        # Get the unique values in the x_column and sort them
        store_locations = np.array(interest_data[location_type].unique())
        store_sales = []
        store_sales1 = []
        store_sales2 = []
        store_sales3 = []
        for item in store_locations:
            location_data = interest_data[interest_data[location_type] == item]
            column_max = location_data[outlet_sales].max()
            store_sales.append(column_max)

        for item in store_locations:
            location_data = interest_data[interest_data[location_type] == item]
            column_min = location_data[outlet_sales].min()
            store_sales1.append(column_min)

        for item in store_locations:
            location_data = interest_data[interest_data[location_type] == item]
            column_mean = location_data[outlet_sales].mean()
            store_sales2.append(column_mean)

        for item in store_locations:
            location_data = interest_data[interest_data[location_type] == item]
            column_mean = location_data[outlet_sales].sum()
            store_sales3.append(column_mean)


        maximum = max(store_sales3) 
        minimum = min(store_sales3)
        max_index = store_sales3.index(max(store_sales3)) 
        min_index = store_sales3.index(min(store_sales3)) 
    
        my_list[4] = f'the highest total sales were of {maximum} of made at {store_locations[max_index]}' 
        my_list[5] = f'the lowest total sales were of {minimum} of made at {store_locations[min_index]}' 


        maximum = max(store_sales) 
        minimum = min(store_sales)
        max_index = store_sales.index(max(store_sales)) 
        min_index = store_sales.index(min(store_sales)) 
        my_list[12] = f'the highest sales is of {maximum} from location {store_locations[max_index]}'
        # Set the x-ticks to the x_values
        my_list[13] = f'so, from this data we have conclude that most profitable location for {preference} is   {store_locations[max_index]}'

        ax.bar(store_locations, store_sales1, width=0.25, label= f'The maximum sales made by {preference}',     align='edge')
        ax.bar(store_locations, store_sales, width=-0.25, label= f'The minimum sales made by {preference}', align=  'edge')
        ax.set_xticks(store_locations)
        # ax.set_yticks(store_sales)

        # Set the title and legend
        ax.set_title(f'sales of the store at all locations {preference}')
        ax.legend()
        timestamp = str(int(time.time()))
        file_name = f"static/New folder/plot_{timestamp}.png"
        fig.savefig(file_name)
        # Close the figure
        plt.close(fig)
        # Show the plot
        return file_name; 


def comparisionOfEachStoreMadeByStore(my_list, uploadedFile): 
    # sales = pd.read_csv('C:/Users/Vilas/Desktop/Train-Set.csv')
    # matching x_axis and y_axis value with column
    column_name = uploadedFile.columns.tolist() 
    my_list1 = [None]*100 
    my_list2 = get_column_name(my_list1, uploadedFile)  
    establishment_year = my_list2[0]
    outlet_type = my_list2[4] 
    outlet_sales = my_list2[5]
    if establishment_year == None or outlet_sales == None or outlet_type == None: 
        my_list[2] = f'The column that you requested is not present in the data'
        return 
    
    
    sales_data = uploadedFile.sort_values(by=establishment_year, ascending=False) # move this line up
    store_names = sales_data[outlet_type].unique()
    print(store_names)
    # Get the data for the selected store type
    # Get the unique values in the x_column and sort them
    store_sales = []
    store_sales1 = []
    store_count = []
    store_sum = []
    fig, ax = plt.subplots(figsize=(8, 6))

    
    for item in store_names:
        store_data = sales_data[sales_data[outlet_type] == item]
        column_max = store_data[outlet_sales].count()
        store_sales.append(column_max)

    for item in store_names:
        store_data = sales_data[sales_data[outlet_type] == item]
        column_max = store_data[outlet_sales].sum()
        store_sum.append(column_max)


    for item in store_names:
        store_data = sales_data[sales_data[outlet_type] == item]
        column_max = store_data[outlet_sales].max()
        store_count.append(column_max)


    for item in store_names:
        store_data = sales_data[sales_data[outlet_type] == item]
        column_max = store_data[outlet_sales].min()
        store_sales1.append(column_max)

    maximum = max(store_count) 
    minimum = min(store_sales1)
    max_index = store_count.index(max(store_count)) 
    min_index = store_sales1.index(min(store_sales1)) 
    
    my_list[2] = f'the highest sales were of {maximum} of made by {store_names[max_index]}' 
    my_list[3] = f'the lowest sales were of {minimum} of made by {store_names[min_index]}'

    maximum1 = max(store_sum) 
    minimum1 = min(store_sum)
    max_index = store_sum.index(max(store_sum)) 
    min_index = store_sum.index(min(store_sum)) 
    my_list[8] = f'the total highest sales were of {maximum1} of made by {store_names[max_index]}'
    my_list[9] = f'the total lowest sales were of {minimum1} of made by {store_names[min_index]}'

    marketData = []
    for item in store_names:
        store_data = sales_data[sales_data[outlet_type] == item]
        column_max = store_data[outlet_sales].sum()
        marketData.append(column_max)
        
    maximum = max(marketData) 
    minimum = min(marketData)
    max_index = marketData.index(max(marketData)) 
    min_index = marketData.index(min(marketData)) 

    my_list[2] = f'the highest sales were of {maximum} of made by {store_names[max_index]}' 
    my_list[3] = f'the lowest sales were of {minimum} of made by{store_names[min_index]}'

    plt.axis('equal')
    plt.pie(marketData,labels=store_names,autopct='%1.1f%%')
    ax.set_title('representation of sales made by each stores') 
    ax.legend()
    timestamp = str(int(time.time()))
    file_name = f"static/New folder/plot_{timestamp}.png"
    fig.savefig(file_name)
    # Close the figure
    plt.close(fig)
    # Show the plot
    return file_name


def salesOfTheStore(store_name, mylst, year, uploadedFile):
    # sales_data = pd.read_csv('C:/Users/Vilas/Desktop/Train-Set.csv')
    # filter data for given store_name
    
    column_names = uploadedFile.columns.tolist()
    my_list = [None]*100 
    my_list1 = get_column_name(my_list, uploadedFile) 
    establishment_year = my_list1[0]
    outlet_type = my_list1[4]
    outlet_sales = my_list1[5]
    product_type = my_list1[3]
    year = uploadedFile[establishment_year].unique() 
    print(year)
    if outlet_type == None or outlet_sales == None or product_type == None: 
        mylst[0] = f'the column you entered does not exist' 
        return

    store_data = uploadedFile[uploadedFile[outlet_type] == store_name]  
    
    # get unique product types and their sales
    product_types = store_data[product_type].unique()
    product_sales = []
    product_sales1 = []
    product_max_sales = []
    product_min_sales = []
    
    for product in product_types:
        product_sales.append(store_data[store_data[product_type] == product][outlet_sales].count())

    for product in product_types:
        product_sales1.append(store_data[store_data[product_type] == product][outlet_sales].sum())

    for product in product_types:
        product_max_sales.append(store_data[store_data[product_type] == product][outlet_sales].max())

    for product in product_types:
        product_min_sales.append(store_data[store_data[product_type] == product][outlet_sales].max())

    print(product_max_sales) 
    print(product_min_sales)
    maximum = max(product_sales1) 
    minimum = min(product_sales1)
    max_index = product_sales1.index(max(product_sales1)) 
    min_index = product_sales1.index(min(product_sales1)) 
    
    mylst[0] = f'the maximum Total sales were of {maximum} of the store {product_types[max_index]}' 
    mylst[1] = f'the minimum Total sales were of {minimum} of the store {product_types[min_index]}'
    mylst[10] = f'The maximum sale were made by {max(product_max_sales)} by the store {product_types[product_max_sales.index(max(product_max_sales))]}'
    mylst[11] = f'The minimum sale were made by {min(product_min_sales)} by the store {product_types[product_min_sales.index(min(product_min_sales))]}'
    # create bar chart
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(product_types, product_sales, label='Total Sales')
    # ax.barh(product_types, product_max_sales, label='Max Sales')
    # ax.barh(product_types, product_min_sales, label='Min Sales')
    ax.set_xlabel('frequency')
    ax.set_ylabel('Product Type')
    ax.set_title(f'Sales at {store_name} by Product Type')
    ax.legend()
    plt.tight_layout()

    # save plot and return file name
    timestamp = str(int(time.time()))
    file_name = f"static/New folder/plot_{timestamp}.png"
    fig.savefig(file_name)
    plt.close(fig)  
    return file_name


# ************************** Store Analysis ********************************

def store_analysis(request, name=None):
    context ={}
    if request.method == 'POST':
        file_name1 = "" 
        file_name2 = "" 
        file_name3 = ""    

        getFile = request.FILES['myFile']
        uploadedFile = pd.read_csv(getFile) 

        store_name = request.POST.get('store_name')
        year = request.POST.get('store_year')
        text_name1 = f'Sales at {store_name} of all product' 
        text_name2 = 'Comparision of sales made by each stores'
        text_name3 = f'sales of the store at all locations for {store_name}'
        my_list = ['']*100 
        if store_name != None: 
            file_name1 = salesOfTheStore(store_name, my_list, year, uploadedFile)  
            if file_name1 != None: 
                context = {'image_url1': f'/{file_name1}'}
            print(context) 
             
            time.sleep(1)
            file_name2 = comparisionOfEachStoreMadeByStore(my_list, uploadedFile)  
            if file_name2 != None: 
                context = {'image_url1': f'/{file_name1}','image_url2': f'/{file_name2}'}
            print(context) 
        
        if store_name != None: 
            time.sleep(1)
            file_name3 = locationWiseSalesOfTheStores(store_name, my_list, uploadedFile) 
            if file_name3 != None: 
                context = {'image_url1': f'/{file_name1}','image_url2': f'/{file_name2}','image_url3': f'/{file_name3}'}
            print(context)
        print(my_list[0]) 
        print(my_list[1])
        # here i have added the insight of the data into the context dictionary
        context = {'image_url1': f'/{file_name1}','image_url2': f'/{file_name2}','image_url3': f'/{file_name3}','name1':text_name1,'name2':text_name2,'name3':text_name3,'insight1':my_list[0],'insight2':my_list[1],'insight3':my_list[2],'insight4':my_list[3],'insight5':my_list[4],'insight6':my_list[5],'insight7':my_list[6],'insight8':my_list[7],'insight11':my_list[8],'insight12':my_list[9],'insight9':my_list[10],'insight10':my_list[11],'insight13':my_list[12],'insight14':my_list[13]} 
        return render(request,'Analysis.html',context)
        # return HttpResponse("submitted")
    else:
        context = {'name': name}
        return render(request, 'store_analysis.html', context)




# ********************** Product Analysis *************************
def product_analysis(request,name=None): 
    context ={}
    if request.method == 'POST': 
        
        getFile = request.FILES['myFile']
        uploadedFile = pd.read_csv(getFile)

        product_type = request.POST.get('product_type')
        year = request.POST.get('year')
        x_axis = request.POST.get('x_axis')
        y_axis = request.POST.get('y_axis')
        
        # defining the string variables. 
        file_name1 = "" 
        file_name2 = "" 
        file_name3 = "" 
        file_name4 = ""
        file_name5 = ""
        file_name6 = ""
        text_name1 = "Sales of a product from the Stores" 
        text_name2 = "Product and " +" "+ y_axis+" " + "Relation"
        
        text_name4 = "Product  Sales  Over  Time" 
        text_name5 = "Product pie chart representation" 
        text_name6 = "Product sales bar representation"
        my_list = ['']*100
        
        if product_type != None and y_axis != None: 
            print('first condition is triggered')
            file_name1 = saleByRegions(year, product_type, my_list, uploadedFile)
            print(file_name1)
            if file_name1 != None: 
                context = {'image_url': f'/{file_name1}'}
            print(context)
            # return render(request,'base.html',context)

        if y_axis != None and x_axis != None: 
            print('second condition is triggered')
            time.sleep(1)
            file_name2 = ProductPriceRelation(x_axis, y_axis, product_type, my_list, uploadedFile)
            print(file_name2)
            context = {'image_url1': f'/{file_name1}','image_url2': f'/{file_name2}'}
            print(context)
            # return render(request,'base.html',context)
            context = {'image_url1': f'/{file_name1}','image_url2': f'/{file_name2}','image_url3': f'/{file_name3}','image_url4': f'/{file_name4}','y_axis':y_axis}
        print(context)

        if x_axis != None and y_axis != None and product_type != None: 
            print("chain saw man") 
            time.sleep(1) 
            file_name5 = PieSaleProduct(year, my_list, uploadedFile)
            context = {'image_url1': f'/{file_name1}','image_url2': f'/{file_name2}','image_url3': f'/{file_name3}','image_url4': f'/{file_name4}','image_url5':f'/{file_name5}'} 

        if x_axis != None and y_axis != None and product_type != None: 
            print("I am Johan Liebert") 
            time.sleep(1) 
            file_name6 = BarSaleProduct(year, my_list, uploadedFile)
            context = {'image_url1': f'/{file_name1}','image_url2': f'/{file_name2}','image_url3': f'/{file_name3}','image_url4': f'/{file_name4}','image_url5':f'/{file_name5}','image_url6':f'/{file_name6}'} 

        # here i am adding the context in the product analysis
        context = {'image_url1': f'/{file_name1}','image_url2': f'/{file_name2}','image_url5':f'/{file_name5}','image_url6':f'/{file_name6}','name1':text_name1,'name2':text_name2,'name4':text_name4,'name5':text_name5,'name6':text_name6,'insight1':my_list[0],'insight2':my_list[1],'insight3':my_list[2],'insight4':my_list[3],'insight5':my_list[4],'insight6':my_list[5],'insight7':my_list[6],'insight8':my_list[7],'insight11':my_list[8],'insight12':my_list[9],'insight9':my_list[10],'insight10':my_list[11],'insight13':my_list[12],'insight14':my_list[13],'insight15':my_list[14],'insight16':my_list[15],'insight17':my_list[16],'insight18':my_list[17],'insight19':my_list[18],'insight20':my_list[19],'insight21':my_list[20],'insight22':my_list[21],'insight23':my_list[22],'insight24':my_list[23]} 
        
        return render(request,'Analysis.html',context)
        # return HttpResponse("SUBMITTED")
    else: 
        return render(request,'product_analysis.html')




# ********************** Product Analysis Graphs *************************************
def saleByRegions(user_year, user_input, my_list, uploadedFile): 
    # sales2 = pd.read_csv('C:/Users/Vilas/Desktop/Train-Set.csv')
    my_list2 = [None]*100
    my_list1 = get_column_name(my_list2, uploadedFile)
    establishment_year = my_list1[0]
    outlet_type = my_list1[4]
    outlet_sales = my_list1[5]
    product_type = my_list1[3]
    if outlet_type == None or outlet_sales == None or product_type == None or establishment_year == None: 
        my_list[0] = 'The column you entered does not exist' 
        return

    sales1 = uploadedFile.loc[0:300, uploadedFile.columns.tolist()]    
    print(type(user_year))
    user_year1 = int(user_year)
    sales = sales1[sales1[establishment_year] == user_year1] 
    print(sales)
    store_names = sales[product_type].unique()
    print(store_names)

    for item in store_names:
        if user_input.lower() in item.lower():
            user_input = item
    print(user_input)
    user_intrest_data = sales[sales[product_type] == user_input] 
    print(sales1)
    location_list = sales1[outlet_type].unique()
    location_max_sale = []
    location_min_sale = []
    location_mean_sale = []
    location_count_sale = []

    for item in location_list:
        location_data = user_intrest_data[user_intrest_data[outlet_type] == item]
        column_max = location_data[outlet_sales].count()
        location_max_sale.append(column_max)

    for item in location_list:
        location_data = user_intrest_data[user_intrest_data[outlet_type] == item]
        column_max = location_data[outlet_sales].max()
        location_count_sale.append(column_max)

    for item in location_list:
        location_data = user_intrest_data[user_intrest_data[outlet_type] == item]
        column_min = location_data[outlet_sales].min()
        location_min_sale.append(column_min)

    for item in location_list:
        location_data = user_intrest_data[user_intrest_data[outlet_type] == item]
        column_mean = location_data[outlet_sales].mean()
        location_mean_sale.append(column_mean)
    fig,ax = plt.subplots()

    for item in location_count_sale: 
        if item == 'nan':
            location_count_sale.index(item) 
            location_count_sale[index] = 0 

    maximum1 = max(location_count_sale) 
    minimum1 = min(location_min_sale) 
    print("hello")
    print(maximum1) 
    print(minimum1)
    max_index = location_count_sale.index(max(location_count_sale)) 
    min_index = location_min_sale.index(min(location_min_sale)) 
    
    # my_list[0] = f'the maximum sales is of {maximum1} and it is made by {location_list[max_index]} during year {user_year}' 
    # my_list[1] = f'the minimum sales is of {minimum1} and it is made by {location_list[min_index]} during year{user_year}'
     
    ax.bar(location_list, location_max_sale,  label=f'product {user_input} maximum sales from {user_year}')
    
    ax.set_xticks(location_list)

    # Set the title and legend
    ax.set_title(f'Outlet sales for {user_input}')
    ax.legend()

    timestamp = str(int(time.time()))
    file_name = f"static/New folder/plot_{timestamp}.png"
    fig.savefig(file_name)
    plt.close(fig)  
    return file_name




def ProductPriceRelation(x_axis, y_axis, product_type, my_list, uploadedFile): 
    # sales2 = pd.read_csv('C:/Users/Vilas/Desktop/Train-Set.csv')
    sales1 = uploadedFile.loc[0:300, uploadedFile.columns.tolist()]
    column_names = sales1.columns.tolist()
    df_sorted = sales1.sort_values(by=x_axis, ascending=False)
    product_type1 = ''

    for item in column_names: 
        if 'product' in item.lower() or 'inlet' in item.lower() or 'item' in item.lower() and 'type' in item.lower(): 
            product_type1 = item 

    if product_type == None: 
        my_list[2] = f'the column you entered does not exist' 
        return


    for item in column_names: 
        if x_axis in item: 
            x_axis = item 
    
    for item in column_names: 
        if y_axis in item: 
            y_axis = item 
    
    product_names = sales1[product_type1].unique()
    for item in product_names: 
        if product_type in item: 
            product_type = item

    sales = df_sorted[df_sorted[product_type1] == product_type] 
    print(sales)
    store_names = sales[product_type1].unique()
    print(store_names)
    # return HttpResponse("HELLO")
    user_interest_data = df_sorted[df_sorted[product_type1] == product_type]
    years = user_interest_data[x_axis].unique()
    product_max_mrp = []
    product_min_mrp = []
    product_mean_mrp = []
    product_sum_mrp = []
    for year in years:
        user_useful_data = user_interest_data[user_interest_data[x_axis] == year]
        column_mean = user_useful_data[y_axis].max()
        product_max_mrp.append(column_mean)

    for year in years:
        user_useful_data = user_interest_data[user_interest_data[x_axis] == year]
        column_mean = user_useful_data[y_axis].sum()
        product_sum_mrp.append(column_mean)

    for year in years:
        user_useful_data = user_interest_data[user_interest_data[x_axis] == year]
        column_mean = user_useful_data[y_axis].min()
        product_min_mrp.append(column_mean)

    for year in years:
        user_useful_data = user_interest_data[user_interest_data[x_axis] == year]
        column_mean = user_useful_data[y_axis].mean()
        product_mean_mrp.append(column_mean)

    maximum1 = max(product_max_mrp) 
    minimum1 = min(product_min_mrp)
    max_index = product_max_mrp.index(max(product_max_mrp)) 
    min_index = product_min_mrp.index(min(product_min_mrp)) 
    
    my_list[2] = f'The maximum {y_axis} is of {maximum1} and it is made when {x_axis} was {years[max_index]}' 
    my_list[3] = f'The minimum {y_axis} is of {minimum1} and it is made when {x_axis} was {years[min_index]}'
    
    fig,ax = plt.subplots()
    print(product_max_mrp)
    print(product_min_mrp)
    print(product_mean_mrp)
    print(years)
    ax.plot(years, product_max_mrp, marker='o')
    ax.plot(years, product_mean_mrp, marker='o')
    ax.plot(years, product_min_mrp, marker='o')
    # ax.legend()

    ax.set_title(f"The line representation of {y_axis} relation with {x_axis} for {product_type}")
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.legend(["Maximu Sales", "Average Sales", "Minimum Sales"],loc='upper left')

    timestamp = str(int(time.time()))
    file_name = f"static/New folder/plot_{timestamp}.png"
    fig.savefig(file_name)
    plt.close(fig)  
    return file_name



def PieSaleProduct(year, my_list, uploadedFile):
    # sales = pd.read_csv('C:/Users/Vilas/Desktop/Train-Set.csv')
    # matching x_axis and y_axis value with column
    
    my_list1 = ["hi"] * 100
    my_list2 = get_column_name(my_list1, uploadedFile)
    establishment_year = my_list2[0]
    product_type = my_list2[3]
    if product_type == None or establishment_year == None: 
        my_list[16] = f'column you entered does not exist' 
        return
    
    sales_data = uploadedFile.sort_values(by=establishment_year, ascending=False) # move this line up
    product_names = sales_data[product_type].unique()
    print(product_names)
    # Get the data for the selected store type
    # Get the unique values in the x_column and sort them
    
    sales_data1 = sales_data[sales_data[establishment_year] == int(year)]
    fig, ax = plt.subplots(figsize=(8, 6))

    marketData = []
    market_max_Data = [] 
    market_min_Data = [] 
    market_sum_Data = [] 

    for item in product_names:
        store_data = sales_data1[sales_data1[product_type] == item]
        column_max = store_data['OutletSales'].count()
        marketData.append(column_max)

    for item in product_names:
        store_data = sales_data1[sales_data1[product_type] == item]
        column_max = store_data['OutletSales'].min()
        market_min_Data.append(column_max)

    for item in product_names:
        store_data = sales_data1[sales_data1[product_type] == item]
        column_max = store_data['OutletSales'].max()
        market_max_Data.append(column_max)

    for item in product_names:
        store_data = sales_data1[sales_data1[product_type] == item]
        column_max = store_data['OutletSales'].sum()
        market_sum_Data.append(column_max)


    maximum1 = max(market_max_Data) 
    minimum1 = min(market_min_Data)
    max_index = market_max_Data.index(max(market_max_Data)) 
    min_index = market_min_Data.index(min(market_min_Data)) 
    
    my_list[16] = f'the maximum OutletSales is of {maximum1} for a year {year} of {product_names[max_index]}' 
     
    my_list[17] = f'the minimum OutletSales is of {minimum1} for a year {year} of {product_names[min_index]}'


    maximum1 = max(market_sum_Data) 
    minimum1 = min(market_sum_Data)
    max_index = market_sum_Data.index(max(market_sum_Data)) 
    min_index = market_sum_Data.index(min(market_sum_Data)) 

    my_list[18] = f'the maximum total OutletSales is of {maximum1} for  a year {year} of  {product_names[max_index]}' 
     
    my_list[19] = f'the minimum total OutletSales is of {minimum1} for a year {year} of {product_names[min_index]}' 

    plt.axis('equal')
    plt.pie(marketData,labels=product_names,autopct='%1.1f%%')
    ax.set_title(f'representation of sales made by each stores in {year}') 
    # ax.legend()
    timestamp = str(int(time.time()))
    file_name = f"static/New folder/plot_{timestamp}.png"
    fig.savefig(file_name)
    # Close the figure
    plt.close(fig)
    # Show the plot
    return file_name


def BarSaleProduct(year, my_list, uploadedFile):
    # sales = pd.read_csv('C:/Users/Vilas/Desktop/Train-Set.csv')
    
    my_list1 = [] 
    my_list2 = get_column_name(my_list1, uploadedFile)
    if my_list2[0] == None or my_list2[3] == None: 
        my_list[20] = f'The column you entered does not exist' 
        return 

    sales_data = uploadedFile.sort_values(by=my_list2[0], ascending=False) # move this line up
    print(sales_data)
    product_names = sales_data[my_list2[3]].unique()
    print(product_names)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sales_data1 = sales_data[sales_data[my_list2[0]] == int(year)]
    print(sales_data1)
    marketData = [] 
    marketData_max = [] 
    marketData_min = [] 
    marketData_total = []
    for item in product_names:
        store_data = sales_data1[sales_data1[my_list2[3]] == item]
        column_max = store_data['OutletSales'].count()
        marketData.append(column_max)

    for item in product_names:
        store_data = sales_data1[sales_data1[my_list2[3]] == item]
        column_max = store_data['OutletSales'].max()
        marketData_max.append(column_max)

    for item in product_names:
        store_data = sales_data1[sales_data1[my_list2[3]] == item]
        column_max = store_data['OutletSales'].sum()
        marketData_total.append(column_max)

    for item in product_names:
        store_data = sales_data1[sales_data1[my_list2[3]] == item]
        column_max = store_data['OutletSales'].min()
        marketData_min.append(column_max)

    maximum1 = max(marketData_max) 
    minimum1 = min(marketData_min)
    max_index = marketData_max.index(max(marketData_max)) 
    min_index = marketData_min.index(min(marketData_min)) 
    

    # adding the insights in it
    my_list[20] = f'the maximum OutletSales is of {maximum1}  of product {product_names[max_index]}' 
     
    my_list[21] = f'the minimum OutletSales is of {minimum1}  of product {product_names[min_index]}'

    maximum1 = max(marketData_total) 
    minimum1 = min(marketData_total)
    max_index = marketData_total.index(max(marketData_total)) 
    min_index = marketData_total.index(min(marketData_total)) 
    
    my_list[22] = f'the maximum OutletSales is of {maximum1}  of product {product_names[max_index]}' 
     
    my_list[23] = f'the minimum OutletSales is of {minimum1}  of product {product_names[min_index]}'

    print(marketData)
    plt.barh(product_names,marketData,label=f'Bar representation of product sold')
    ax.set_title(f'representation of sales made by each stores in {year}') 
    ax.legend() 
    timestamp = str(int(time.time()))
    file_name = f"static/New folder/plot_{timestamp}.png"
    fig.savefig(file_name)
    # Close the figure
    plt.close(fig)
    # Show the plot
    return file_name
