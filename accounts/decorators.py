from django.http import HttpResponse
from django.shortcuts import redirect
def authenticated_user(class_view):
    def inner(request,*args,**kwargs):
            if request.user.is_authenticated:
                return redirect('/')
            else:
                return class_view(request,*args,**kwargs)
    return inner

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group=''
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are not allowed to view this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group == "admin":
            return view_func(request,*args,**kwargs)
        if group =="customers":
            return redirect('/user/')
    return wrapper_func