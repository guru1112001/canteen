
from django.shortcuts import render, redirect
from .utils import cookieCart, cartData, guestOrder
from .models import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import OrderForm, CreateUserForm, OrderItemForm, CustomerForm, Order2Form, ProductForm

import json
import datetime


# @user_only
def menu(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'food/menu.html', context)


def breakfast(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'food/breakfast.html', context)


def lunch(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'food/lunch.html', context)


def todayspl(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'food/todayspl.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    form = OrderForm()
    if request.method == 'POST':
        print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            delivery = request.POST['take_away']
            request.session['delivery'] = delivery
            form.save()
            print('delivery:', delivery)
        return redirect('checkout')

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'form': form}
    return render(request, 'food/cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, }
    return render(request, 'food/checkout.html', context)


def UpdateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    order.take_away = request.session['delivery']

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    return JsonResponse('Payment complete', safe=False)


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'food/register.html', context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('menu')
        else:
            messages.info(request, 'Username or Password is incorrect ')

    context = {}
    return render(request, 'food/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('menu')
