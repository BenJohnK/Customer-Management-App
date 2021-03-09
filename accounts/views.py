from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from .forms import OrderForm,CustomerForm,CreateUserForm
from django.forms import inlineformset_factory
from .filter import OrderFilter
from django.contrib.auth.forms import UserCreationForm



# Create your views here.

def login(request):
    return render(request,"accounts/login.html",{})

def register(request):
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,"accounts/register.html",{'form':form})

def index(request):
    customers=Customer.objects.all()
    total_customers=customers.count()
    orders=Order.objects.all().order_by('-id')[:5]
    total_orders=Order.objects.all().count()
    delivered=Order.objects.filter(status="Delivered").count()
    pending=Order.objects.filter(status="Pending").count()
    return render(request,"accounts/dashboard.html",{'customers':customers,'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending,'total_customers':total_customers})

def products(request):
    products = Product.objects.all()
    return render(request,"accounts/products.html",{'products':products})

def customers(request,id):
    customer=Customer.objects.get(id=id)
    total_orders=customer.orders
    orders=customer.order_set.all().order_by('-id')
    my_filter=OrderFilter(request.GET,queryset=orders)
    orders=my_filter.qs
    return render(request,"accounts/customer.html",{'customer':customer,'orders':orders,'total_orders':total_orders,'myfilter':my_filter})
    
def createOrder(request,id):
    customer=Customer.objects.get(id=id)
    OrderFormSet=inlineformset_factory(Customer,Order, fields=('product','status'), extra=7)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form=OrderForm(initial={'customer':customer})
    if request.method=="POST":

        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    return render(request,"accounts/ordercreateform.html",{'formset':formset})

def updateOrder(request,id):
    order=Order.objects.get(id=id)
    form=OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,"accounts/orderform.html",{'form':form})

def deleteOrder(request,id):
    order=Order.objects.get(id=id)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    return render(request,"accounts/deleteorder.html")

def createCustomer(request):
    form=CustomerForm()
    if request.method=="POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,"accounts/customerform.html",{'form':form})

def updateCustomer(request,id):
    customer=Customer.objects.get(id=id)
    form=CustomerForm(instance=customer)
    if request.method=="POST":
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,"accounts/customerform.html",{'form':form})

def deleteCustomer(request,id):
    customer=Customer.objects.get(id=id)
    if request.method=="POST":
        customer.delete()
        return redirect('/')
    return render(request,"accounts/deletecustomer.html",{'customer':customer})


