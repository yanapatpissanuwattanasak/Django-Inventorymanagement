from django.shortcuts import render,redirect
from .models import Tables,Personal,Product,Manufacturer,History_input,Product_output,preorder,Basket,Order,store_stock,saled,Shelf,product_shelf,check,lost_list,Group_analysis,history_lost,history_product_shelf,History_move,Group_store,Month_qty_ago,Month_qty_now
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from urllib.parse import urlencode
from localStoragePy import localStoragePy
from datetime import date ,datetime
from django.db import connection
from datetime import  timedelta
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django import forms
from .forms import ImageForm
from .models import Image

#asdasd
# Create your views here.
localStorage = localStoragePy('store', 'json')

def pie_chart(request):
    labels = ["กลุ่มสินค้า A : "+g_analysis.A,"กลุ่มสินค้า B : "+g_analysis.B,"กลุ่มสินค้า C : "+g_analysis.C]
    if g_analysis.A =="":
        g_analysis.A = "No Product"
    elif g_analysis.B =="":
        g_analysis.B = "No Product"
    elif g_analysis.C =="":
        g_analysis.C = "No Product"
    data = [g_analysis.numA,g_analysis.numB,g_analysis.numC]

    return render(request, 'pie_chart.html', {
        'labels': labels,
        'data': data,
    })

def cal_month_qty_ago():
    product = Product_output.objects.all()
    output = Month_qty_ago.objects.all()
    for i in output:
        e = Month_qty_ago.objects.get(product_code=i.product_code)
        e.Jan = 0
        e.Feb = 0
        e.Mar = 0
        e.Apr = 0
        e.May = 0
        e.Jun = 0
        e.Jul = 0
        e.Aug = 0
        e.Sep = 0
        e.Oct = 0
        e.Nov = 0
        e.Dec = 0
        e.save()
    for j in product:
        #print(j.product_code+"wow")
        output = Month_qty_ago.objects.get(product_code=j.product_code)
        #cal = Product_output.objects.get(product_code=j.product_code)
        x = j.date_output.month
        y = j.date_output.year
        y_ago = date.today().year-1
        #print("x ="+str(x))
        #print("qty="+str(j.product_quantity))
        if x==1 and y==y_ago :
            output.Jan+=j.product_quantity
        elif x==2 and y==y_ago :
            output.Feb+=j.product_quantity
        elif x==3 and y==y_ago:
            output.Mar+=j.product_quantity
        elif x==4 and y==y_ago:
            output.Apr+=j.product_quantity
        elif x==5 and y==y_ago:
            output.May+=j.product_quantity
        elif x==6 and y==y_ago :
            output.Jun+=j.product_quantity
        elif x==7 and y==y_ago:
            output.Jul+=j.product_quantity
        elif x==8 and y==y_ago:
            output.Aug+=j.product_quantity
        elif x==9 and y==y_ago:
            output.Sep+=j.product_quantity
        elif x==10 and y==y_ago:
            output.Oct+=j.product_quantity
        elif x==11 and y==y_ago:
            output.Nov+=j.product_quantity
        elif x==12 and y==y_ago :
            output.Dec+=j.product_quantity
        output.save()

def cal_month_qty_now():
    product = Product_output.objects.all()
    output = Month_qty_now.objects.all()
    for i in output:
        e = Month_qty_now.objects.get(product_code=i.product_code)
        e.Jan = 0
        e.Feb = 0
        e.Mar = 0
        e.Apr = 0
        e.May = 0
        e.Jun = 0
        e.Jul = 0
        e.Aug = 0
        e.Sep = 0
        e.Oct = 0
        e.Nov = 0
        e.Dec = 0
        e.save()
    for j in product:
        #print(j.product_code+"wow")
        output = Month_qty_now.objects.get(product_code=j.product_code)
        #cal = Product_output.objects.get(product_code=j.product_code)
        x = j.date_output.month
        y = j.date_output.year
        y_now = date.today().year
        #print("x ="+str(x))
        #print("qty="+str(j.product_quantity))
        if x==1 and y==y_now :
            output.Jan+=j.product_quantity
        elif x==2 and y==y_now :
            output.Feb+=j.product_quantity
        elif x==3 and y==y_now:
            output.Mar+=j.product_quantity
        elif x==4 and y==y_now:
            output.Apr+=j.product_quantity
        elif x==5 and y==y_now:
            output.May+=j.product_quantity
        elif x==6 and y==y_now :
            output.Jun+=j.product_quantity
        elif x==7 and y==y_now:
            output.Jul+=j.product_quantity
        elif x==8 and y==y_now:
            output.Aug+=j.product_quantity
        elif x==9 and y==y_now:
            output.Sep+=j.product_quantity
        elif x==10 and y==y_now:
            output.Oct+=j.product_quantity
        elif x==11 and y==y_now:
            output.Nov+=j.product_quantity
        elif x==12 and y==y_now :
            output.Dec+=j.product_quantity
        output.save()

def g_analysis():
    output = Month_qty_ago.objects.all()
    dict = {}
    total=0
    g_analysis.A = ""
    g_analysis.B = ""
    g_analysis.C = ""
    g_analysis.numA = 0
    g_analysis.numB = 0
    g_analysis.numC = 0
    for i in output:
        e = Month_qty_ago.objects.get(product_code=i.product_code)
        total+= e.Jan+e.Feb+e.Mar+e.Apr+e.May+e.Jun+e.Jul+e.Aug+e.Sep+e.Oct+e.Nov+e.Dec
        e.total = total
        e.save()
        dict[i.product_code]=total
        total =0
    totally = 0
    for i in output:
        totally+=i.total
    for i in output:
        if(i.total == 0 ) :
            x = 0
        else :
            x = int(i.total/totally*100)
        print(type(x))
        print("x"+str(x))
        if x in range(80,101):
            g_analysis.numA += i.total
            g_analysis.A += str(i.product_code)+" "
            print(g_analysis.A+"is A")
            g = Group_analysis.objects.get(product_code=i.product_code)
            g.group = "A"
            g.save()
        elif x in range(40,80):
            g_analysis.numB += i.total
            g_analysis.B += str(i.product_code)+" "
            print(g_analysis.B+"is B")
            g = Group_analysis.objects.get(product_code=i.product_code)
            g.group = "B"
            g.save()
        elif x in range(0,40):
            g_analysis.numC += i.total
            g_analysis.C += str(i.product_code)+" "
            print(g_analysis.C+"is C")
            g = Group_analysis.objects.get(product_code=i.product_code)
            g.group = "C"
            g.save()
class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = '__all__'

def update_groupstore():
    user = Personal.objects.get(username=localStorage.getItem("user"))
    for i in store_stock.objects.filter(store_id=user.shop_name) :
        try :
            Group_store.objects.get(product_code=i.product_code,shop_id=i.store_id)
            pass
        except :
            product = Group_store()
            product.product_code = i.product_code
            product.shop_id = i.store_id
            product.qty = 0
            product.group = "C"
            product.save()
    sums =  0 
    for i in Group_store.objects.filter(shop_id=user.shop_name) :
        sums += i.qty
    for i in Group_store.objects.filter(shop_id=user.shop_name) :
        total = 0 
        for j in saled.objects.filter(product_code=i.product_code) :
            if(date.today() - j.date < timedelta(days=60) ) :
                total += j.qty
        i.qty = total
        if ((total*1.0) > 0.8 * (sums*1.0)) :
            print(total,sums)
            print("A")
            i.group = "A"
        elif ((total*1.0) > 0.4 * (sums*1.0)) :
            print(total,sums)
            print("B")
            i.group = "B"
        else :
            print("C")
            i.group = "C"
        i.save()
def contact_complete(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    topic = request.POST['topic']
    detail = request.POST['detail']
    send_mail = settings.EMAIL_HOST_USER
    pass_mail = settings.EMAIL_HOST_PASSWORD
    print(send_mail)
    print(pass_mail)

    msg = MIMEMultipart()
    msg['Subject'] = topic
    msg['From'] = ''
    msg['To'] = ''
    email_message = "ชื่อผู้แจ้ง : " + fname + ' ' + lname + '\n' + "Email : " + email +'\n' + detail
    body = email_message
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
        server.starttls()
        try:
            server.login("yanapat.pi@ku.th","@0868464543Bright")
            server.sendmail(send_mail, send_mail, text)
            print("Send Mail Sucessfully")
        except:
            print("Incorrect account or password")
        finally:
            print("Quit Server")
            server.quit()
    except:
        print("server not found")

    if(localStorage.getItem("user") is not None):
        return redirect('/contact',{'name' :localStorage.getItem("user"),'fullname':user.fullname})
    else :

        return redirect('/login')
def index(request,product_id):
    if(localStorage.getItem("user") is not None):
        product = Product.objects.get(product_code=product_id)
        index.product_id = product.product_code
        return render(request,'index.html',{'name' :localStorage.getItem("user"),'product':product,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')
def dashboard(request):
    user = Personal.objects.get(username=localStorage.getItem("user"))
    if(user.rank == "admin") :
        Low = len(Product.objects.filter(prodect_status='Low'))
        Empty = len(Product.objects.filter(prodect_status='Empty'))
        uncheck = len(Shelf.objects.filter(status='unCheck'))
        A = len(Group_analysis.objects.filter(group="A"))
        B = len(Group_analysis.objects.filter(group="B"))
        C = len(Group_analysis.objects.filter(group="C"))
        group = [A,B,C]
        stockstatus = [Low,Empty,uncheck]
        print(uncheck)
        inputs = history_product_shelf.objects.all().order_by('-date','-id')[:3]
        top = Group_analysis.objects.all().order_by('-month_qty')[:3]
        order = Order.objects.all().filter(status="Success")
        late = 0
        late_all = len(order)
        month = date.today().month
        for i in order :
            if i.date_sended - i.date > timedelta(days=3) :
                    late += 1
        if(late != 0 and late_all !=0) :
            per_late = (late * 1.0)/(late_all*1.0)*100
        else :
            per_late = 0
        lists = history_product_shelf.objects.all()
        sums = 0
        for i in lists :
            if(i.date.month == month) :
                sums += i.total
        pic = []
        for i in Group_analysis.objects.all().order_by('-month_qty')[:3] :
                pic.append(Image.objects.get(id= Product.objects.get(product_code=i.product_code).product_image))

        sum_lost = 0 
        all_lost = history_lost.objects.all()
        for i in all_lost :
            if i.check_date.month  == month :
                sum_lost += (int(i.qty)*int(Product.objects.get(product_code=i.product_code).product_selling))
              
        
        return render(request,'dashboard.html',{'fullname':user.fullname,'name' :localStorage.getItem("user"),'stockstatus':stockstatus,'inputs':inputs,'group':group,'top':top,'per_late':per_late,'sums':sums,'sum_lost':sum_lost,'pic':pic})
    else :
        update_groupstore()
        good = len(store_stock.objects.filter(status = "good"))
        low = len(store_stock.objects.filter(status = "Low"))
        empty = len(store_stock.objects.filter(status = "Empty"))
        status = [good,low,empty]
        A = len(Group_store.objects.filter(shop_id=user.shop_name,group="A"))
        B = len(Group_store.objects.filter(shop_id=user.shop_name,group="B"))
        C = len(Group_store.objects.filter(shop_id=user.shop_name,group="C"))
        group = [A,B,C]
        top = Group_store.objects.all().order_by('-qty')[:3]
        order = Order.objects.all().filter(status="Success",shop_name=user.shop_name)
        pic = []
        late = 0
        late_all = len(order)
        month = date.today().month
        for i in order :
            if i.date_sended - i.date > timedelta(days=3) :
                    late += 1
        per_late = (late * 1.0)/(late_all*1.0)*100
        print(late_all,late,per_late)
        cost = 0 
        for i in Order.objects.filter(shop_name=user.shop_name) :
            for j in Basket.objects.filter(status=i.order_id) :
                cost += (j.qty * Product.objects.get(product_code=j.product_code).product_cost)
        for i in Group_store.objects.all().order_by('-qty')[:3] :
                pic.append(Image.objects.get(id= Product.objects.get(product_code=i.product_code).product_image))
        return render(request,'dashboard_owner.html',{'fullname':user.fullname,'name' :localStorage.getItem("user"),'status':status,'group':group,'top':top,'per_late':per_late,'cost':cost,'pic':pic})
def billtoshelf(request) :
    product =  History_move.objects.last()
    print(product)
    name = Product.objects.get(product_code=product.product_code).product_name
    return render(request, 'AddtoShelf.html',{'name' :localStorage.getItem("user"),'product': product,'name':name,'fullname':user.fullname})
class ChartData(APIView): 
    authentication_classes = [] 
    permission_classes = []
    def get(self, request, format = None):
        product_id = index.product_id
        #print (product_id)
        cursor = connection.cursor()
        #query = 'select * from project_app_month_qty where product_code = "'+product_id+'"'
        #query = 'select project_app_product_output.product_quantity from project_app_product_output where product_code = "'+product_id+'"'
        query = 'select project_app_month_qty_ago.Jan,project_app_month_qty_ago.Feb,project_app_month_qty_ago.Mar,project_app_month_qty_ago.Apr,project_app_month_qty_ago.May,project_app_month_qty_ago.Jun,project_app_month_qty_ago.Jul,project_app_month_qty_ago.Aug,project_app_month_qty_ago.Sep,project_app_month_qty_ago.Oct,project_app_month_qty_ago.Nov,project_app_month_qty_ago.Dec from project_app_month_qty_ago where product_code = "'+product_id+'"'
        query2 = 'select project_app_month_qty_now.Jan,project_app_month_qty_now.Feb,project_app_month_qty_now.Mar,project_app_month_qty_now.Apr,project_app_month_qty_now.May,project_app_month_qty_now.Jun,project_app_month_qty_now.Jul,project_app_month_qty_now.Aug,project_app_month_qty_now.Sep,project_app_month_qty_now.Oct,project_app_month_qty_now.Nov,project_app_month_qty_now.Dec from project_app_month_qty_now where product_code = "'+product_id+'"'

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.execute(query2)
        results2 = cursor.fetchall()
        #print(results)
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
        chartLabel = "จำนวนที่ขายได้"
        chartdata = []
        chartdata2 = []
        for i in results:
            #print("i"+str(i))
            for j in i:
                chartdata.append(j)
        for i in results2:
            #print("i"+str(i))
            for j in i:
                chartdata2.append(j)

        #print(chartdata)
        data = { 
                     "labels":labels, 
                     "chartLabel":chartLabel, 
                     "chartdata":chartdata,
                     "chartdata2":chartdata2, 
                }
        
        return Response(data)

def updatestock() :
    list_product = Product.objects.all()
    for i in list_product :
        try :
            total = 0
            for j in product_shelf.objects.all().filter(product_code=i.product_code) :
                total += j.qty
            i.product_balance = total
            i.save()
        except :
            i.product_balance = 0
            i.save()


def auto_lost(request) :
    for i in lost_list.objects.all() :
        p_s = product_shelf.objects.get(product_code=i.product_code,shelf_id=i.shelf_id)
        p_s.qty -= i.qty
        lost = history_lost()
        lost.product_code = i.product_code
        p_s.save()
        lost.qty = i.qty
        dates = date.today()
        if dates.day > 1 and dates.day < 15 :
            lost.check_date = datetime(dates.year, dates.month, 1)
            lost.save()
        else :
            lost.check_date = datetime(dates.year, dates.month, 16)
            lost.save()
    update_shelf()
    updatestock()

    return redirect('/showzone')



def filter_month():
    #print(str(get_year.year_num))
    #print(str(get_month.month_num))
    y = date.today().year
    m = date.today().month-1
    if(y%4 == 0):
        if(m == 2):
            stop_date = date(y,2,29)
            print(stop_date)
        else:
            try:
                stop_date = date(y,m,31)
                print("normal")
            except:
                stop_date = date(y,m,30)
                print("fixed")
    else:
        if(m == 2):
            stop_date = date(y,2,28)
            print(stop_date)
        else:
            try:
                stop_date = date(y,m,31)
                print("normal")
            except:
                stop_date = date(y,m,30)
                print("fixed")
    start_date = date(y,m,1)
    #start_date = date(2021,3,1)
    #stop_date = date(2021,3,31)
    product = Product_output.objects.all()
    output = Group_analysis.objects.all()
    for j in output:
        p = Group_analysis.objects.get(product_code=j.product_code)
        p.month_qty=0
        p.profit=0
        p.profit_per=0
        p.save()
    for i in product :
        print(i.product_code)

        output = Group_analysis.objects.get(product_code=i.product_code)
        cal = Product.objects.get(product_code=i.product_code)
        if(i.date_output >= start_date and i.date_output <= stop_date ):
            #print(i.date_output)
            output.month_qty += i.product_quantity
            output.profit = (cal.product_selling-cal.product_cost)*output.month_qty
        output.save()
def analysis(request):
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == "admin") :


            filter_month()

            cal_month_qty_ago()
            g_analysis()
            pie_chart(request)
            cal_month_qty_now()
            cursor = connection.cursor()
            cursor.execute('select project_app_group_analysis.product_code,project_app_product.product_name,project_app_group_analysis.month_qty,project_app_product.product_selling*project_app_group_analysis.month_qty,project_app_group_analysis.profit,project_app_group_analysis.group from project_app_product join project_app_group_analysis on project_app_product.product_code = project_app_group_analysis.product_code  ')
            itemlist = cursor.fetchall()
            return render(request, 'analysis.html',{'name' :localStorage.getItem("user"),'itemlist':itemlist,'fullname':user.fullname})
        else :
            return render(request,'error.html')
    else :
        return redirect('/login')
def sum_lost(request):
    lost_list.objects.all().delete()

    

    list_product = product_shelf.objects.all()
    for p in list_product :
        try :
            pro_check = check.objects.get(product_code=p.product_code,shelf_id=p.shelf_id)
            if(p.qty > pro_check.qty):
                item = lost_list()
                item.product_code = p.product_code
                item.shelf_id = p.shelf_id
                item.qty = int(p.qty) - int(pro_check.qty)
                item.save()
            else :
                pass
        except :
            pass
    return redirect('/sumarize')

def add_check(request):
    if request.POST.get('shelf_id') and request.POST.get('product_id') and request.POST.get('qty') :
        shelf_id = request.POST.get('shelf_id')
        product_id = request.POST.get('product_id')
        qty = request.POST.get('qty')

        try :
            pros = Product.objects.get(product_code=product_id)
            shelfs = product_shelf.objects.get(shelf_id=shelf_id)
        except :
            print("exit")
            return redirect('/checkstock')
        try :
            obj = check.objects.get(product_code=product_id,shelf_id=shelf_id)
            obj.qty = qty
            obj.save()
        except :
            obj = check()
            obj.product_code = product_id
            obj.shelf_id = shelf_id
            obj.qty = qty
            obj.employee = localStorage.getItem("user")
            obj.date = date.today()
            obj.time = datetime.now()
            obj.save()
            return redirect('/checkstock')
    return redirect('/checkstock')

def update_status():
    product = Product.objects.all()
    for i in product :
        
        output = Product_output.objects.filter(product_code=i.product_code)
        qty = 0
        for j in output :
            if(j.date_output > date.today() - timedelta(days=30)):
            
                qty += j.product_quantity
        if(i.product_balance == 0) :
            pro = Product.objects.get(product_code=i.product_code)
            pro.prodect_status = "Empty"
            pro.save()

        elif(((qty/30)*i.product_send_time)+1 >= i.product_balance):
            pro = Product.objects.get(product_code=i.product_code)
            pro.prodect_status = "Low"
            pro.save()
        
        else :
                pro = Product.objects.get(product_code=i.product_code)
                pro.prodect_status = "good"
                pro.save()
        
def update_status_owner():
    store = store_stock.objects.all()
    user = Personal.objects.get(username=localStorage.getItem("user"))
    
    for i in store :
        output = saled.objects.filter(product_code=i.product_code,shop_name=user.shop_name)
        qty = 0
        for j in output :
            if(j.date > date.today() - timedelta(days=30)):
                qty += j.qty
        
        if(int(i.qty) == 0) :
            print("EiEi1")
            st = store_stock.objects.get(product_code=i.product_code,store_id=i.store_id)
            st.status = "Empty"
            st.save()
        elif(((qty/30)*2) >= int(i.qty)):
            print("EiEi2")
            st = store_stock.objects.get(product_code=i.product_code,store_id=i.store_id)
            st.status = "Low"
            st.save()
        else :
            print("EiEi3")
            st = store_stock.objects.get(product_code=i.product_code,store_id=i.store_id)
            st.status = "good"
            st.save()

            


    


def received(request):
        
        order_id = request.POST.get('order_id')
        
        order = Order.objects.get(order_id=order_id)
        order.date_sended = request.POST.get('date_receive')
        order.status = "Success"
        order.save()
        
        busket = Basket.objects.filter(status=order_id)
        for i in busket:
            print("eiei1")
            try:
                store = store_stock.objects.get(product_code=i.product_code)
                store.qty += int(i.qty)
                product = Product.objects.get(product_code= i.product_code)
                product.product_balance -= int(i.qty)
                print(product.product_balance)
                product.save()
                store.save()
                print("eiei2")
            except:
                store = store_stock()
                store.product_code = i.product_code
                store.qty = i.qty
                user = Personal.objects.get(username=i.employee)
                store.store_id = user.shop_name

                product = Product.objects.get(product_code= i.product_code)
                product.product_balance -= int(i.qty)
                print(product.product_balance)
                product.save()
                store.save()
                print("eiei3")
        
        
        return redirect('/store_receiving')


def detail_owner(request,id) :
    product = Product.objects.get(product_code = id)
    return render(request, 'detail_owner.html',{'product':product,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})

def store_detail(request):
    return render(request, 'store_detail.html',{'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})

def store_receiving(request):
    return render(request, 'store_receiving.html',{'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})

def store_preorder(request):
    return render(request, 'store_preorder.html',{'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})

def store_analysis(request):
    return render(request, 'store_analysis.html',{'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})

def re_check():
    ch = check.objects.all()
    dates = 0
    for i in ch :
        dates = i.date.day
    date_me = date.today().day
    if date_me < 15 and dates >=15 :
        for i in ch:
            i.delete()
        for i in Shelf.objects.all():
            i.status = "unCheck"
            i.save()
        for i in product_shelf.objects.all() :
            i.status = "unCheck"
            i.save()
    elif date_me >= 15 and dates < 15 :
        for i in ch:
            i.delete()
        for i in Shelf.objects.all():
            i.status = "unCheck"
            i.save()
        for i in product_shelf.objects.all():
            i.status = "unCheck"
            i.save()

def check_detail(request):
    return render(request, 'check_detail.html')

def shelf(request):
    user = Personal.objects.get(username=localStorage.getItem("user"))
    if(user.rank == "admin") :
        return render(request, 'shelf.html',{'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return render(request, 'error.html')

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
            shelf.code7_9 = "G"
            shelf.value = request.POST.get('value')
            A = shelf.code1_4 + shelf.code5_6 + request.POST.get('code7_9')
            shelf.code = A
            shelf.status = "unCheck"
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
    user = Personal.objects.get(username=localStorage.getItem("user"))
    if(user.rank == "admin") :
        checks = True
        results = Shelf.objects.all()
        re_check()
        for i in results :
            items = product_shelf.objects.filter(shelf_id=i.code)
            print(items)
            
            for item in items :
                try :
                    check.objects.get(product_code=item.product_code,shelf_id=item.shelf_id)
                    item.status = "Checked"
                    item.save()
                    pass
                except :
                    try :
                        eiei = Shelf.objects.get(code=item.shelf_id)
                        eiei.status = 'unCheck'
                        eiei.save()
                        checks = False
                        break
                    except :
                        pass
            if(checks) :
                eiei = Shelf.objects.get(code=i.code)
                eiei.status = 'Checked'
            
                eiei.save()
        status = []
        for i in Shelf.objects.all() :
                if i.valueremain > i.value/3.0 :
                    status.append("Good")
                elif i.valueremain == 0:
                    status.append("Empty")
                else :
                    status.append("Low")
        
        update_shelf()
    else :
        return render(request,'error.html')
    return render(request, 'shelf_order.html',{'results' : results,'status':status,'fullname':user.fullname})

def select_id_shelf(request):
    return render(request, 'select_id_shelf.html',{'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})

def moveTo(request):
    product_code = request.POST['code']
    productInShelf = product_shelf.objects.filter(product_code=product_code)
    return render(request, 'moveTo.html',{'productInShelf':productInShelf})

def select(request,id):
    user = Personal.objects.get(username=localStorage.getItem("user"))
    product_sh = product_shelf.objects.get(id=id)
    product = [product_sh.id,product_sh.product_code,product_sh.shelf_id,product_sh.qty]
    qty = int(product_sh.qty)
    cursor = connection.cursor()
    cursor.execute('select * from project_app_shelf WHERE project_app_shelf.valueremain >'+str(qty)+' AND project_app_shelf.code != "'+product_sh.shelf_id+'"')
    shelf = cursor.fetchall()
    return render(request, 'moveTo2.html',{'shelf':shelf,'product':product,'fullname':user.fullname})


def move(request,id,product_id,shelf_id,qty,shelf_id_2):
    try :
        product = product_shelf.objects.get(product_code=product_id,shelf_id=shelf_id_2)
        product.qty += qty
        product.save()
        item = product_shelf.objects.get(id=id)
       
        item.delete()
    except :
        product = product_shelf()
        product.product_code = product_id
        product.shelf_id = shelf_id_2
        product.qty = qty
        product.status = "unCheck"
        product.save()
        item = product_shelf.objects.get(id=id)
        
        item.delete()
    his = History_move()
    his.product_code = product_id
    his.qty = int(qty)
    his.from_shelf = shelf_id
    his.to_shelf = shelf_id_2
    his.employee = Personal.objects.get(username=localStorage.getItem("user")).fullname
    his.save()
    updatestock()
    return redirect('/shelf')

def history_move(request):
    user = Personal.objects.get(username=localStorage.getItem("user"))
    lists = History_move.objects.all()
    return render(request, 'history_move.html',{'name' :localStorage.getItem("user"),'lists':lists,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})


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
    user = Personal.objects.get(username=localStorage.getItem("user")).fullname
    if(user.rank != "admin") :
        if  request.POST['code'] and request.POST['balance'] :
            Preorder = preorder()
            Preorder.product_code = request.POST['code']
            Preorder.balance = request.POST['balance'] 
            Preorder.employee = localStorage.getItem("user")
            Preorder.date =  date.today()
            Preorder.save()
            return redirect('/')
    else :
         return render(request,'error.html',{'name' :localStorage.getItem("user")})
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
        shop_id = Personal.objects.get(username= localStorage.getItem("user")).shop_name
        cursor.execute('select project_app_product.product_code,project_app_product.product_name,project_app_saled.qty,project_app_saled.total,project_app_saled.date from project_app_product join project_app_saled on project_app_product.product_code = project_app_saled.product_code WHERE project_app_saled.shop_name = "'+shop_id+'"')
        results = cursor.fetchall()
        return render(request,'history_output.html',{'name' :localStorage.getItem("user"),'tables':results,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

def sale_output_owner(request,validation = True):
    if(localStorage.getItem("user") is not None):
        try:
            user = Personal.objects.get(username=localStorage.getItem("user"))
            product_code = request.POST['code1']
            product_quantity = request.POST['quantity']
            date_output = request.POST['date_output']
            store = store_stock.objects.get(product_code=product_code,store_id=user.shop_name)
            store.qty -= int(product_quantity)
            store.save()

            
            product = Product_output()
            product.product_code = product_code
            product.product_quantity = product_quantity
            product.date_output = date_output
            product.save()
                

            sale = saled()
            sale.product_code = product_code
            sale.shop_name = user.shop_name
            sale.employee = user.username
            sale.date =  date_output
            sale.qty = int(product_quantity)
            sale.total = Product.objects.get(product_code=product_code).product_selling * int(product_quantity)
            sale.save()
            print("EiEI Sale raw")
            
            
            return redirect('/output')
        except:
            return render(request,'sale_output_owner.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
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
    if(user.rank != "admin") :
        user = Personal.objects.get(username=localStorage.getItem("user"))
        cursor = connection.cursor()
        cursor.execute('select project_app_basket.id,project_app_product.product_code,project_app_product.product_name,project_app_basket.qty,project_app_basket.status from project_app_product join project_app_basket on project_app_product.product_code = project_app_basket.product_code WHERE project_app_basket.employee ="'+user.username+'" AND project_app_basket.status = "waiting" ')
        results = cursor.fetchall()
        print(results)
        return render(request, 'Request_list.html',{'user':user,'results':results,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return render(request, 'error.html',{'user':user})

def order_product(request):
    orderss = Basket.objects.filter(employee=localStorage.getItem("user") ,status="waiting")
    num = 0
    for i in Order.objects.all():
        num = int(i.order_id)
    print(num+1)
    for i in orderss:
        orders = Basket.objects.get(id = i.id)
        
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

    all_list = Basket.objects.filter(status=(num+1))
    print(all_list)
    for i in all_list :
        qty = i.qty
        for j in product_shelf.objects.filter(product_code=i.product_code) :
            if(qty < j.qty) :
                j.qty -= qty 
                j.save()
                break
            else :
                qty -= j.qty
                j.delete()
                
    updatestock()
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
    updatestock()
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
                update_status()
                return render(request,'stock.html',{'name' :localStorage.getItem("user"),'manufact':manufact,'products':results,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
                print("2")
            else:
                
                print("2")
                #cursor.execute('select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.type,project_app_product.cost,project_app_product.selling,project_app_product.size,project_app_store_stock.qty from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code ) WHERE  product_code LIKE "'+search_words+'" OR  product_name LIKE "'+search_words+'"'')
                
                if(search_words == "%%%%"):
                    
                    cursor = connection.cursor()
                    print("asdas")
                    cursor.execute('select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.product_type,project_app_product.product_cost,project_app_product.product_selling,project_app_product.product_size,project_app_store_stock.qty,project_app_store_stock.status from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code WHERE project_app_store_stock.store_id = "'+user.shop_name+'" ')
                     
                    results = cursor.fetchall()
                    print("1")
                    
                    
                else :
                    print("EiEi")
                    cursor = connection.cursor()
                    
                    cursor.execute('select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.product_type,project_app_product.product_cost,project_app_product.product_selling,project_app_product.product_size,project_app_store_stock.qty,project_app_store_stock.status from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code WHERE  (project_app_store_stock.product_code LIKE "'+search_words+'" OR  project_app_product.product_name LIKE "'+search_words+'") AND project_app_store_stock.store_id = "'+user.shop_name+'" ')
                    results = cursor.fetchall()
                    
                    #results = results.objects.raw('select * from (select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.product_type,project_app_product.product_cost,project_app_product.product_selling,project_app_product.product_size,project_app_store_stock.qty from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code) WHERE  project_app_store_stock.product_code LIKE "'+search_words+'" OR  project_app_product.product_name LIKE "'+search_words+'"')
                   
                    
                    #cursor.execute('select * from project_app_product WHERE  product_code LIKE "'+search_words+'" OR  product_name LIKE "'+search_words+'"')
                    
                    #products = results.objects.raw('select * from project_app_product WHERE  product_code LIKE "'+search_words+'" OR  product_name LIKE "'+search_words+'"')
                    
                update_status_owner()
                return render(request,'store_stock.html',{'name' :localStorage.getItem("user"),'manufact':manufact,'products':results,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})

        except:
            print("2")
            if(user.rank == 'admin') :
                results = Product.objects.all()
                update_status()
                return render(request,'stock.html',{'name' :localStorage.getItem("user"),'manufact':manufact,'products':results,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
            else :
                cursor = connection.cursor()
                print("asdas")
                cursor.execute('select project_app_store_stock.store_id,project_app_store_stock.product_code,project_app_product.product_name,project_app_product.product_type,project_app_product.product_cost,project_app_product.product_selling,project_app_product.product_size,project_app_store_stock.qty,project_app_store_stock.status from project_app_store_stock join project_app_product on project_app_store_stock.product_code = project_app_product.product_code WHERE project_app_store_stock.store_id = "'+user.shop_name+'" ')
                     
                results = cursor.fetchall()
                update_status_owner()
                return render(request,'store_stock.html',{'name' :localStorage.getItem("user"),'manufact':manufact,'products':results,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
            
       
        
        return redirect('/')
    else :
        return redirect('/login')
def detail(request,product_id):
    if(localStorage.getItem("user") is not None):
        product = Product.objects.get(product_code=product_id)
        image = Image.objects.get(id=int(product.product_image))

        return render(request,'detail.html',{'name' :localStorage.getItem("user"),'product':product,'image':image,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')
def detail_user(request,user_id):
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == "admin") :
            user = Personal.objects.get(username = user_id)
            return render(request,'detail_user.html',{'name' :localStorage.getItem("user"),'user':user,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
             return render(request,'error.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

def to_shelfs(request) :
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == "admin") :
            product_code = request.POST['code']
            product_balance = request.POST['balance']
            product = [product_code,product_balance]
            #same = product_shelf.objects.filter(product_code=product_code)
            #inshelf = Shelf.objects.all()
            cursor = connection.cursor()
            cursor.execute('select project_app_shelf.code,project_app_shelf.value,project_app_shelf.valueremain,project_app_product_shelf.product_code from project_app_product_shelf join project_app_shelf on project_app_product_shelf.shelf_id = project_app_shelf.code WHERE project_app_shelf.valueremain >'+product_balance+' AND project_app_product_shelf.product_code = "'+product_code+'"')
            inshelf = cursor.fetchall()
            #outshelf = Shelf.objects.all()
            cursor2 = connection.cursor()
            cursor2.execute('select * from project_app_shelf')
            outshelf = cursor2.fetchall()
            print(inshelf,outshelf)
            return render(request,'to_shelfs.html',{'name' :localStorage.getItem("user"),'inshelf':inshelf,'outshelf':outshelf,'product': product,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
            return render(request,'error.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})

def input(request,validation = True):
    check = True
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == "admin") :
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
                history.history_user = Personal.objects.get(username=localStorage.getItem("user")).fullname
                history.save()
                product.save()
                return redirect('/import_product')

            except :
                if(check) :
                    return render(request,'input.html',{'name' :localStorage.getItem("user"),'validate' : True,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
                else :
                    return render(request,'input.html',{'name' :localStorage.getItem("user"),'validate' : False,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
            return render(request,'error.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

def order_detail(request,id):
    if(localStorage.getItem("user") is not None):
        cursor = connection.cursor()
        cursor.execute('select project_app_product.product_code,project_app_product.product_name,project_app_basket.qty from project_app_product join project_app_basket on project_app_product.product_code = project_app_basket.product_code WHERE project_app_basket.status = "'+id+'"')
        results = cursor.fetchall()
        return render(request,'order_detail.html',{'name' :localStorage.getItem("user"),'tables':results,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else:
        return redirect('/login')

def save_product(request,product_code,amount,shelf_id):
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == 'admin'):
            try :
                product = product_shelf.objects.get(product_code=product_code,shelf_id=shelf_id)
                product.qty +=int(amount)
                product.save()
                save = Product.objects.get(product_code=product_code)
                save.product_balance += int(amount)
                save.save()
                history = history_product_shelf()
                history.product_code = product_code
                history.qty = int(amount)
                history.shelf_id = shelf_id
                history.total = int(amount)*int(save.product_cost)
                history.date = date.today()
                history.user = Personal.objects.get(username=localStorage.getItem("user")).fullname
                history.save()
                update_shelf()
                return redirect('/input')
            except :
                product = product_shelf()
                product.product_code = product_code
                product.qty = amount
                product.shelf_id = shelf_id
                product.status = "unCheck"
                product.save()
                save = Product.objects.get(product_code=product_code)
                save.product_balance += int(amount)
                save.save()
                history = history_product_shelf()
                history.product_code = product_code
                history.qty = int(amount)
                history.shelf_id = shelf_id
                history.total = int(amount)*int(save.product_cost)
                history.date = date.today()
                history.user = Personal.objects.get(username=localStorage.getItem("user")).fullname
                history.save()
                update_shelf()
                return redirect('/input')
            
        else :
            return render(request,'error.html',{'name' :localStorage.getItem("user")})


def detail_shelf(request,shelf_id) :
    cursor = connection.cursor()
    cursor.execute('select P.product_code,P.product_name,P.product_type,P.product_size,PS.qty,PS.status from project_app_product_shelf AS PS join project_app_product AS P on P.product_code = PS.product_code WHERE PS.shelf_id = "'+shelf_id+'"')
    items = cursor.fetchall()
    return render(request,'detail_shelf.html',{'name' :localStorage.getItem("user"),'items':items,'shelf_id':shelf_id,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
def update_shelf():
    shelf = Shelf.objects.all()
    for item in shelf :
        p = product_shelf.objects.filter(shelf_id=item.code)
        item.valueremain = item.value  
        for i in p:
            
            item.valueremain -= int(i.qty)
        item.save()
        if item.valueremain > (item.value*1.0)/3.0 :
            item.value_status = "G"
        elif item.valueremain < (item.value*1.0)/3.0 and  item.valueremain > 0 :
            item.value_status = "L"
        else :
            item.value_status = "E"
        item.save()

def import_product(request):
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank != 'admin'):
            results =Order.objects.filter(shop_name=user.shop_name)
            return render(request,'history_import_owner.html',{'name' :localStorage.getItem("user"),'tables':results,'fullname':user.fullname,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
            
            cursor = connection.cursor()
            cursor.execute('select project_app_product.product_code,project_app_product.product_name,project_app_product.product_type,project_app_history_product_shelf.qty,project_app_product.product_cost,project_app_history_product_shelf.id,project_app_history_product_shelf.total,project_app_history_product_shelf.shelf_id,project_app_history_product_shelf.date from project_app_product join project_app_history_product_shelf on project_app_product.product_code = project_app_history_product_shelf.product_code')
            results = cursor.fetchall()
            return render(request,'history_import.html',{'name' :localStorage.getItem("user"),'tables':results,'fullname':user.fullname,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
            
    else :
        return redirect('/login')


def checkstock(request):
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == "admin") :
            return render(request,'checkstock.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
            return render(request,'error.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

def status_send(request):
    
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == "admin") :
            orders = Order.objects.all()
            return render(request,'status_send.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
            orders = Order.objects.all()
            return render(request,'status_send.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

def status_request_send(request):
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == "admin") :
            orders = Order.objects.all()
            return render(request,'status_request_send.html',{'name' :localStorage.getItem("user"),'orders':orders,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
            orders = Order.objects.all()
            return render(request,'status_request_send.html',{'name' :localStorage.getItem("user"),'orders':orders,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

def shipping(request):
    if(localStorage.getItem("user") is not None):
       
        return render(request,'shipping.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
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
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == 'admin'):
            return render(request,'select_history.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
             return render(request,'select_history_owner.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        
        return redirect('/login')


def user_list(request):
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == "admin") :
            list_user = Personal.objects.all().filter(rank = "")
            return render(request,'user_list.html',{'name' :localStorage.getItem("user"),'list_user':list_user,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
            return render(request,'error.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        
    else :
        
        return redirect('/login')

def Transmission_history(request):
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == admin) :
            return render(request,'Transmission_history.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
            return redirect('/login')
    else :
        
        return redirect('/login')

def history_import(request):
    if(localStorage.getItem("user") is not None):
        return render(request,'history_import.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        
        return redirect('/login')

def register_employee(request):
    
    return render(request,'registration.html')

def edit_item(request):
    if(localStorage.getItem("user") is not None):
        edit_item.form = ImageForm(request.FILES)
        menu = Manufacturer.objects.all()
        return render(request,'edit_product.html',{'menu':menu,'form': edit_item.form,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')


def edit(request,id):
    if(localStorage.getItem("user") is not None):
        menu = Manufacturer.objects.all()
        product = Product.objects.get(product_code=id)
        return render(request,'edit.html',{'menu':menu,'product':product,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')
def submit_edit(request):
    if(localStorage.getItem("user") is not None):
        pc = request.POST['product_code']
        print(pc)
        product = Product.objects.get(product_code=pc)
        product.product_name = request.POST['product_name']
        product.product_type = request.POST['product_type']
        product.product_size = request.POST['product_size']
        product.product_send_time = request.POST['product_send_time']
        product.product_cost = request.POST['product_cost']
        product.product_selling = request.POST['product_selling']
        product.save()
    return redirect('/input')


def submit_product(request):
    product_code = request.POST['product_code']
    product_name = request.POST['product_name']
    product_type = request.POST['product_type']
    product_size = request.POST['product_size']
    product_send_time = request.POST['product_send_time']
    product_cost = request.POST['product_cost']
    product_selling = request.POST['product_selling']
    product_desc = request.POST['product_desc']
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
    if( request.POST['select'] == "No") :

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
        product.product_image= str(Image.objects.last().id)
        product.product_fact_name = fact_name
        product.save()
    else :
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
        product.product_image= str(Image.objects.last().id)
        product.product_fact_name = request.POST['select']
        product.save()
    #manufact.save()
    group = Group_analysis()
    group.product_code = product_code
    group.save()

    month_ago = Month_qty_ago()
    month_ago.product_code = product_code
    month_ago.save()

    month_now = Month_qty_now()
    month_now.product_code = product_code
    month_now.save()
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
                    print(personal.fullname)
                    print(pwd)
                    print(personal.identification)
                    print(personal.phone)
                    print(personal.address_id)
                    print(personal.address_t)
                    print(personal.address_a)
                    print(personal.address_city)
                    print(personal.address_post)
                    

                    user.save()
                    return redirect('/')
                else:
                    return redirect('/register')
            return redirect('/register')
        return redirect('/register') 
        
        
        
        
    return redirect('/')
def checkemployee(request):
    if(localStorage.getItem("user") is not None):
        cursor = connection.cursor()
        cursor.execute('select project_app_check.product_code,project_app_product.product_name,project_app_check.shelf_id,project_app_check.qty,project_app_check.date,project_app_check.time,project_app_check.employee from project_app_check join project_app_product on project_app_check.product_code = project_app_product.product_code')
        results = cursor.fetchall()
        return render(request,'checkemployee.html',{'name' :localStorage.getItem("user"),'results':results,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

def sumarize(request):
    if(localStorage.getItem("user") is not None):
        cursor = connection.cursor()
        cursor.execute('select project_app_lost_list.product_code,project_app_product.product_name,project_app_lost_list.shelf_id,project_app_lost_list.qty from project_app_product join project_app_lost_list on project_app_product.product_code = project_app_lost_list.product_code')
        results = cursor.fetchall()
        return render(request,'sumarize.html',{'name' :localStorage.getItem("user"),'results':results,'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

def contact(request):
    if(localStorage.getItem("user") is not None):
        user = Personal.objects.get(username=localStorage.getItem("user"))
        if(user.rank == "admin") :
            return render(request,'contact.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        else :
            #return render(request,'error.html',{'name' :localStorage.getItem("user")})
           return render(request,'contact_owner.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

def lost_item(request):
    if(localStorage.getItem("user") is not None):
        return render(request,'lost_item.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
        
        
    else :
        return redirect('/login')

def check_detail(request):
    if(localStorage.getItem("user") is not None):
       
        return render(request,'check_detail.html',{'name' :localStorage.getItem("user"),'fullname':Personal.objects.get(username=localStorage.getItem("user")).fullname})
    else :
        return redirect('/login')

