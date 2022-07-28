from django.http import HttpResponse
from django.shortcuts import redirect

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('menu')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def user_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if  request.user.is_staff:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
