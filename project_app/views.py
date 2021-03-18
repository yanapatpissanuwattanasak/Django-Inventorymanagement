from django.shortcuts import render,redirect
from .models import Tables,Personal,Product,Manufacturer,History_input,Product_output,preorder,Basket,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from urllib.parse import urlencode
from localStoragePy import localStoragePy
from datetime import date
from django.db import connection



# Create your views here.
localStorage = localStoragePy('store', 'json')

def received(request):
        order_id = request.POST.get('order_id')
        
        order = Order.objects.get(order_id=order_id)
        order.date_sended = request.POST.get('date_receive')
        order.status = "Success"
        order.save()
        return redirect('/store_receiving')

def store_stock(request):
    return render(request, 'store_stock.html')

def store_detail(request):
    return render(request, 'store_detail.html')

def store_receiving(request):
    return render(request, 'store_receiving.html')

def store_preorder(request):
    return render(request, 'store_preorder.html')

def store_analysis(request):
    return render(request, 'store_analysis.html')

def analysis(request):
    return render(request, 'analysis.html')

def check_detail(request):
    return render(request, 'check_detail.html')

def shelf(request):
    return render(request, 'shelf.html')

def c_d_shelf(request):
    return render(request, 'create_delete_shelf.html')

def c_shelf(request):
    return render(request, 'create_shelf.html')

def d_shelf(request):
    data = Shelf.objects.all()
    return render(request, 'delete_shelf.html',{'shelf':data})

def addShelf(request):
    if request.method == 'POST':
        if request.POST.get('code1_4') and request.POST.get('code5_6') and request.POST.get('code7_9') and request.POST.get('value'):
            shelf = Shelf()
            shelf.code1_4 = request.POST.get('code1_4')
            shelf.code5_6 = request.POST.get('code5_6')
            shelf.code7_9 = request.POST.get('code7_9')
            shelf.value = request.POST.get('value')
            A = shelf.code1_4 + shelf.code5_6 + shelf.code7_9
            shelf.code = A
            shelf.save()

            return render(request, 'create_delete_shelf.html')
        else:
            return render(request, 'create_delete_shelf.html')
    else:
        return render(request, 'create_delete_shelf.html')


def deleteshelf(request,code):
    a = Shelf.objects.get(code=code)
    a.delete()
    return redirect('/cdshelf')

def show_zone(request):
    return render(request, 'show_zone.html')

def select_id_shelf(request):
    return render(request, 'select_id_shelf.html')

def history_move(request):
    return render(request, 'history_move.html')


def cancleImport(request,id):
    a = History_input.objects.get(id = id) 
    product = Product.objects.get(product_code= a.history_product_code)
    a.delete()
    product.product_balance -= a.history_balance
    product.save()
    return redirect('/import_product')
def cancleRequest(request,id):
    
    a = Basket.objects.get(id = id) 
    a.delete()
    
    
    return redirect('/Request1_owner/Request_list')

def owner_preorder(request):
    if  request.POST['code'] and request.POST['balance'] :
        Preorder = preorder()
        Preorder.product_code = request.POST['code']
        Preorder.balance = request.POST['balance'] 
        Preorder.employee = localStorage.getItem("user")
        Preorder.date =  date.today()
        Preorder.save()
        return redirect('/')
    return redirect('')

def login(request,validation = True):
   
    if(localStorage.getItem("user") is not None):
        return redirect('/')
    else:
        try :
            username = request.POST['username']
            password = request.POST['password']
        except :
            return render(request,'login.html',{'validation':validation})
        print(username,password)
        person = Personal.objects.get(username = username)
        print(person)
        if(person.rank == "") :
                return render(request,'login.html',{'validation':False})
        user = authenticate(username=username, password=password)
        print()
        if user is  None:
            return render(request,'login.html',{'validation':False})
        else:
            localStorage.setItem("user" , username)
            return redirect('/')
    return render(request,'login.html',{'validation':validation})

def logout(request):
    localStorage.clear()
    return redirect('/login')

def submit_user(request,user_id) :
    p = Personal.objects.get(username = user_id)
    
    try :
        if request.POST['employee'] == "on":
            p.rank = "employee"
    except: pass
    try :
        if request.POST['owner'] == "on" :
            p.rank = "owner"
    except: pass
    try :
        if request.POST['admin'] == "on" :
            p.rank = "admin"
    except: pass
    
    
    p.save()
    return redirect('/user_list')
def output_product(request):
    if(localStorage.getItem("user") is not None):
        cursor = connection.cursor()
        cursor.execute('select project_app_product.product_code,project_app_product.product_name,project_app_product.product_type,project_app_product_output.product_quantity,project_app_product.product_selling,project_app_product_output.id,project_app_product.product_selling*project_app_product_output.product_quantity,project_app_product_output.date_output from project_app_product join project_app_product_output on project_app_product.product_code = project_app_product_output.product_code')
        results = cursor.fetchall()
        return render(request,'history_output.html',{'name' :localStorage.getItem("user"),'tables':results})
    else :
        return redirect('/login')

def sale_output_owner(request,validation = True):
    if(localStorage.getItem("user") is not None):
        try:
            product_code = request.POST['code1']
            product_quantity = request.POST['quantity']
            date_output = request.POST['date_output']
            print("EiEI")
            product_output = Product_output()
            product = Product.objects.get(product_code = product_code)
            product.product_balance -= int(product_quantity)
            product_output.product_code = product_code
            product_output.product_quantity = product_quantity
            product_output.date_output = date_output
            product_output.save()
            product.save()
            #manufact.save()
            return redirect('/output')
        except:
            return render(request,'sale_output_owner.html',{'name' :localStorage.getItem("user")})
    else :
        return redirect('/login')


def Request1_owner(request):
    return render(request, 'Request1_owner.html',{'validate' : True})
def Request1_owner_error(request):
    return render(request, 'Request1_owner.html',{'validate' : False})

def Request_value(request,validate = True):
    if request.POST['code'] :
        product_code = request.POST['code']
        try :
            product = Product.objects.get(product_code=product_code)
        except :
            return redirect('/Request1_owner_error')

        return render(request, 'Request_value.html',{'product':product})
    else:
        return redirect('/Request1_owner/Request_list')

def Request_list(request):
    user = Personal.objects.get(username=localStorage.getItem("user"))
    cursor = connection.cursor()
    cursor.execute('select project_app_basket.id,project_app_product.product_code,project_app_product.product_name,project_app_basket.qty,project_app_basket.status from project_app_product join project_app_basket on project_app_product.product_code = project_app_basket.product_code WHERE project_app_basket.employee ="'+user.username+'" AND project_app_basket.status = "waiting" ')
    results = cursor.fetchall()
    print(results)
    return render(request, 'Request_list.html',{'user':user,'results':results})

def order_product(request):
    orders = Basket.objects.get(employee=localStorage.getItem("user") ,status="waiting")
    
    
    num = len(Order.objects.all())
    orders.status = num+1
    orders.save()
    order = Order()
    order.order_id = num+1
    order.employee = localStorage.getItem("user")
    order.shop_name = Personal.objects.get(username=localStorage.getItem("user")).shop_name
    order.date = date.today()
    order.date_sended = date.today()
    order.status = "Sending"
    order.save()
    return redirect('/Request1_owner/Request_list')

def go_login(request):
    username = request.POST['username']
    password = request.POST['password']
    # return render(request,'stock.html',{'username':username,'pwd':password})
    print("go_login")
    
    query_string =  urlencode({'username': username,'pwd' : password})
    url = '{}?{}'.format('/', query_string)
    return redirect(url)

def submit_request(request):
    print(request.POST['code'])
    if request.POST['code'] and request.POST['amount'] :
        try :
            item = Basket.objects.get(product_code = request.POST['code'] , status = "waiting")
            item.qty = item.qty + int(request.POST['amount'])
            if(item.qty > Product.objects.get(product_code=request.POST['code']).product_balance) :
                item.qty = Product.objects.get(product_code=request.POST['code']).product_balance
            item.save()
        except:
            item = Basket()
            item.product_code = request.POST['code']
            item.qty = int(request.POST['amount'])
            if(item.qty > Product.objects.get(product_code=request.POST['code']).product_balance) :
                item.qty = Product.objects.get(product_code=request.POST['code']).product_balance
            item.employee = localStorage.getItem("user")
            item.status = "waiting"
            item.save()
        return redirect('/Request1_owner/Request_list')

def stock(request,manufact = None):
    if(localStorage.getItem("user") is not None):
        username = localStorage.getItem("user")
        user = Personal.objects.get(username=username)

        
        try :
            search_words = "%%"+request.GET['search']+"%%"
            print(search_words)
                
            if(user.rank == 'admin') :
                if(search_words == "%%%%"):
                        results = Product.objects.all()
                else :
                      
                        results = Product.objects.raw('select * from project_app_product WHERE  product_code LIKE "'+search_words+'" OR  product_name LIKE "'+search_words+'"')
                        
                return render(request,'stock.html',{'name' :localStorage.getItem("user"),'manufact':manufact,'products':results})
                print("2")
            else:
                
                print("2")
                #cursor.execute('select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.type,project_app_product.cost,project_app_product.selling,project_app_product.size,project_app_store_stock.qty from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code ) WHERE  product_code LIKE "'+search_words+'" OR  product_name LIKE "'+search_words+'"'')
                
                if(search_words == "%%%%"):
                    
                    cursor = connection.cursor()
                    print("asdas")
                    cursor.execute('select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.product_type,project_app_product.product_cost,project_app_product.product_selling,project_app_product.product_size,project_app_store_stock.qty from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code WHERE project_app_store_stock.store_id = "'+user.shop_name+'" ')
                     
                    results = cursor.fetchall()
                    print("1")
                    
                    
                else :
                    print("EiEi")
                    cursor = connection.cursor()
                    
                    cursor.execute('select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.product_type,project_app_product.product_cost,project_app_product.product_selling,project_app_product.product_size,project_app_store_stock.qty from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code WHERE  (project_app_store_stock.product_code LIKE "'+search_words+'" OR  project_app_product.product_name LIKE "'+search_words+'") AND project_app_store_stock.store_id = "'+user.shop_name+'" ')
                    results = cursor.fetchall()
                    
                    #results = results.objects.raw('select * from (select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.product_type,project_app_product.product_cost,project_app_product.product_selling,project_app_product.product_size,project_app_store_stock.qty from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code) WHERE  project_app_store_stock.product_code LIKE "'+search_words+'" OR  project_app_product.product_name LIKE "'+search_words+'"')
                   
                    print("EiEi")
                    #cursor.execute('select * from project_app_product WHERE  product_code LIKE "'+search_words+'" OR  product_name LIKE "'+search_words+'"')
                    
                    #products = results.objects.raw('select * from project_app_product WHERE  product_code LIKE "'+search_words+'" OR  product_name LIKE "'+search_words+'"')
                    print("EiEi")
                return render(request,'store_stock.html',{'name' :localStorage.getItem("user"),'manufact':manufact,'products':results})

        except:
            print("2")
            if(user.rank == 'admin') :
                results = Product.objects.all()
                   
                return render(request,'stock.html',{'name' :localStorage.getItem("user"),'manufact':manufact,'products':results})
            else :
                cursor = connection.cursor()
                print("asdas")
                cursor.execute('select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.product_type,project_app_product.product_cost,project_app_product.product_selling,project_app_product.product_size,project_app_store_stock.qty from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code WHERE project_app_store_stock.store_id = "'+user.shop_name+'" ')
                     
                results = cursor.fetchall()
                   
                return render(request,'store_stock.html',{'name' :localStorage.getItem("user"),'manufact':manufact,'products':results})
            
       
        
        return redirect('/')
    else :
        return redirect('/login')
def detail(request,product_id):
    if(localStorage.getItem("user") is not None):
        product = Product.objects.get(product_code=product_id)
       
        return render(request,'detail.html',{'name' :localStorage.getItem("user"),'product':product})
    else :
        return redirect('/login')
def detail_user(request,user_id):
    if(localStorage.getItem("user") is not None):
        
        user = Personal.objects.get(username = user_id)
        return render(request,'detail_user.html',{'name' :localStorage.getItem("user"),'user':user})
    else :
        return redirect('/login')

def input(request,validation = True):
    check = True
    if(localStorage.getItem("user") is not None):
        try:
            product_code = request.POST['code']
            product_balance = request.POST['balance']
            today = date.today()
            check = False
            product = Product.objects.get(product_code = product_code)
            product.product_balance += int(product_balance)
            history = History_input()
            history.history_product_code = product_code
            history.history_balance = product_balance
            print(product.product_cost)
            print(product_balance)
            history.history_total = product.product_cost * int(product_balance)
            print(history.history_total)
            history.history_date = today
            history.history_user = localStorage.getItem("user")
            history.save()
            product.save()
            return redirect('/import_product')

        except :
            if(check) :
                return render(request,'input.html',{'name' :localStorage.getItem("user"),'validate' : True})
            else :
                return render(request,'input.html',{'name' :localStorage.getItem("user"),'validate' : False})
    else :
        return redirect('/login')

def import_product(request):
    if(localStorage.getItem("user") is not None):
        cursor = connection.cursor()
        cursor.execute('select project_app_product.product_code,project_app_product.product_name,project_app_product.product_type,project_app_history_input.history_balance,project_app_product.product_cost,project_app_history_input.id,project_app_history_input.history_total,project_app_history_input.history_date from project_app_product join project_app_history_input on project_app_product.product_code = project_app_history_input.history_product_code')
        results = cursor.fetchall()
        return render(request,'history_import.html',{'name' :localStorage.getItem("user"),'tables':results})
    else :
        return redirect('/login')


def checkstock(request):
    if(localStorage.getItem("user") is not None):
       
        return render(request,'checkstock.html',{'name' :localStorage.getItem("user")})
    else :
        return redirect('/login')

def status_send(request):
    
    if(localStorage.getItem("user") is not None):
        orders = Order.objects.all()
        return render(request,'status_send.html',{'name' :localStorage.getItem("user")})
    else :
        return redirect('/login')

def status_request_send(request):
    if(localStorage.getItem("user") is not None):
        orders = Order.objects.all()
        return render(request,'status_request_send.html',{'name' :localStorage.getItem("user"),'orders':orders})
    else :
        return redirect('/login')

def shipping(request):
    if(localStorage.getItem("user") is not None):
       
        return render(request,'shipping.html',{'name' :localStorage.getItem("user")})
    else :
        return redirect('/login')

def update(request,id):
    
    # name = request.POST['name']
    # name = request.POST['desc']
    a = Tables.objects.get(id = id)
    print(a.name,a.desc,a.id)
    a.name = 'qweqweqwe'
    a.desc = 'qweqweqwe'
    print(a.name,a.desc,a.id)
    a.save()
    return redirect('/')

def delete(request,id):
    
    # name = request.POST['name']
    # name = request.POST['desc']
    a = Tables.objects.get(id = id) 
    a.delete()
        
       
    return redirect('/')
def insert(request):
    if request.POST['name'] and request.POST['desc']:
        a = Tables()
        a.name = request.POST['name']
        a.desc = request.POST['desc']
        a.save()
      

    return redirect('/')

def open_history(request,):
    if(localStorage.getItem("user") is not None):
        
        return render(request,'select_history.html',{'name' :localStorage.getItem("user")})
    else :
        
        return redirect('/login')


def user_list(request):
    if(localStorage.getItem("user") is not None):
        list_user = Personal.objects.all().filter(rank = "")
        return render(request,'user_list.html',{'name' :localStorage.getItem("user"),'list_user':list_user})
    else :
        
        return redirect('/login')

def Transmission_history(request):
    if(localStorage.getItem("user") is not None):
        return render(request,'Transmission_history.html',{'name' :localStorage.getItem("user")})
    else :
        
        return redirect('/login')

def history_import(request):
    if(localStorage.getItem("user") is not None):
        return render(request,'history_import.html',{'name' :localStorage.getItem("user")})
    else :
        
        return redirect('/login')

def register_employee(request):
    
    return render(request,'registration.html')

def edit_item(request):
    if(localStorage.getItem("user") is not None):
        return render(request,'edit_product.html')
    else :
        return redirect('/login')

def submit_product(request):
    product_code = request.POST['product_code']
    product_name = request.POST['product_name']
    product_type = request.POST['product_type']
    product_size = request.POST['product_size']
    product_send_time = request.POST['product_send_time']
    product_cost = request.POST['product_cost']
    product_selling = request.POST['product_selling']
    product_desc = request.POST['product_desc']


    #manufact
    fact_name = request.POST['fact_name']
    fact_id = request.POST['fact_id']
    fact_t = request.POST['fact_t']
    fact_a = request.POST['fact_a']
    fact_city = request.POST['fact_city']
    fact_post = request.POST['fact_post']
    fact_email = request.POST['fact_email']
    fact_phone = request.POST['fact_phone']
    fact_desc  = request.POST['fact_desc']
    fact_serialandBatch = request.POST['fact_serialandBatch']

    fact = Manufacturer()
    fact.fact_name = fact_name
    fact.fact_id = fact_id
    fact.fact_t = fact_t
    fact.fact_a = fact_a
    fact.fact_city = fact_city
    fact.fact_post = fact_post
    fact.fact_email = fact_email
    fact.fact_phone = fact_phone
    fact.fact_desc = fact_desc
    fact.fact_serialandBatch = fact_serialandBatch
    fact.save()

    product = Product()
    product.product_code = product_code
    product.product_name = product_name
    product.product_type = product_type
    product.product_size = product_size
    product.product_send_time = product_send_time
    product.product_cost = product_cost
    product.product_selling = product_selling
    product.product_desc = product_desc
    product.prodect_status = ""
    product.product_balance = 0
    product.save()
    #manufact.save()
    return redirect('/')
    


def create_account(request):
    
    
    if request.POST['username'] and request.POST['email'] and request.POST['pass'] :
        username = request.POST['username']
        email = request.POST['email']
        pwd = request.POST['pass']
        try:
            User.objects.get(username=username)
            
        except:
            try :
                User.objects.get(email = email)
            except:
                user = authenticate(username=username, password=pwd)

                if user is None:
                    user = User.objects.create_user(username,email,pwd)

                    personal = Personal()
                    personal.username = username
                    personal.rank = ""
                    personal.email = email
                    personal.fullname = request.POST['name']
                    personal.identification = request.POST['id']
                    personal.phone = request.POST['phone']
                    personal.shop_name = request.POST['shop']
                    personal.address_id = request.POST['house_number']
                    personal.address_t = request.POST['t']
                    personal.address_a =request.POST['o']
                    personal.address_city = request.POST['j']
                    personal.address_post = request.POST['post_id']
                    personal.address_desc = request.POST['desc']
                    personal.save()
                    user.save()
                    return redirect('/')
                else:
                    return redirect('/register')
            return redirect('/register')
        return redirect('/register') 
        
        
        
        
    return redirect('/')
def checkemployee(request):
    if(localStorage.getItem("user") is not None):
       
        return render(request,'checkemployee.html',{'name' :localStorage.getItem("user")})
    else :
        return redirect('/login')

def sumarize(request):
    if(localStorage.getItem("user") is not None):
       
        return render(request,'sumarize.html',{'name' :localStorage.getItem("user")})
    else :
        return redirect('/login')

def contact(request):
    if(localStorage.getItem("user") is not None):
       
        return render(request,'contact.html',{'name' :localStorage.getItem("user")})
    else :
        return redirect('/login')

def lost_item(request):
    if(localStorage.getItem("user") is not None):
       
        return render(request,'lost_item.html',{'name' :localStorage.getItem("user")})
    else :
        return redirect('/login')

def check_detail(request):
    if(localStorage.getItem("user") is not None):
       
        return render(request,'check_detail.html',{'name' :localStorage.getItem("user")})
    else :
        return redirect('/login')

