from django.shortcuts import render,redirect
from .models import Tables

# Create your views here.
def login(request):
    return render(request,'login.html')

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

def register_employee(request):
    return render(request,'registration.html')
