from django.http import HttpResponse
from django.shortcuts import redirect #redirect function redirect us the given page 

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_staff:# agr staff/employee ni h toh usse redirect kr do menu m 
            return redirect('menu')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def user_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if  request.user.is_staff:#agr user staff h ya employee h toh usse redirect kr do dashboard pe 
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
