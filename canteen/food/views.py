from django.shortcuts import render
from .utils import cookieCart, cartData, guestOrder
#@user_only
def menu(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems':cartItems}
    return render(request, 'food/menu.html', context)
