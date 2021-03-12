from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from .forms import OrderForm,CustomerForm,CreateUserForm
from django.forms import inlineformset_factory
from .filter import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from . decorators import authenticated_user,allowed_users,admin_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
 

# Create your views here.
@authenticated_user
def loginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Incorrect Username or Password!')
            return redirect('/login/')
    return render(request,"accounts/login.html",{})

def logoutPage(request):
    logout(request)
    return redirect('/login/')

@authenticated_user
def register(request):
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name="customers")
            user.groups.add(group)
            username=form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+username)
            return redirect('/login/')
    return render(request,"accounts/register.html",{'form':form})

@login_required(login_url='/login/')
@admin_only
def index(request):
    customers=Customer.objects.all()
    total_customers=customers.count()
    orders=Order.objects.all().order_by('-id')[:5]
    total_orders=Order.objects.all().count()
    delivered=Order.objects.filter(status="Delivered").count()
    pending=Order.objects.filter(status="Pending").count()
    user=False
    return render(request,"accounts/dashboard.html",{'customers':customers,'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending,'total_customers':total_customers,'user':user})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    user=False
    return render(request,"accounts/products.html",{'products':products,'user':user})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def customers(request,id):
    customer=Customer.objects.get(id=id)
    total_orders=customer.orders
    orders=customer.order_set.all().order_by('-id')
    my_filter=OrderFilter(request.GET,queryset=orders)
    orders=my_filter.qs
    user=False
    return render(request,"accounts/customer.html",{'customer':customer,'orders':orders,'total_orders':total_orders,'myfilter':my_filter,'user':user})
    
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,id):
    customer=Customer.objects.get(id=id)
    OrderFormSet=inlineformset_factory(Customer,Order, fields=('product','status'), extra=7)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    user=False
    # form=OrderForm(initial={'customer':customer})
    if request.method=="POST":

        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    return render(request,"accounts/ordercreateform.html",{'formset':formset,'user':user})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,id):
    order=Order.objects.get(id=id)
    form=OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    user=False
    return render(request,"accounts/orderform.html",{'form':form,'user':user})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,id):
    order=Order.objects.get(id=id)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    user=False
    return render(request,"accounts/deleteorder.html",{'user':user})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form=CustomerForm()
    if request.method=="POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    user=False
    return render(request,"accounts/customerform.html",{'form':form,'user':user})

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request,id):
    customer=Customer.objects.get(id=id)
    form=CustomerForm(instance=customer)
    if request.method=="POST":
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    user=False
    return render(request,"accounts/customerform.html",{'form':form,'user':user})
    
@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request,id):
    customer=Customer.objects.get(id=id)
    if request.method=="POST":
        customer.delete()
        return redirect('/')
    user=False
    return render(request,"accounts/deletecustomer.html",{'customer':customer,'user':user})

@login_required(login_url='/login/')
def userPage(request):
    total_orders=Order.objects.all().count()
    delivered=Order.objects.filter(status="Delivered").count()
    pending=Order.objects.filter(status="Pending").count()
    user=True
    return render(request,"accounts/userPage.html",{'total_orders':total_orders,'delivered':delivered,'pending':pending,'user':user})



