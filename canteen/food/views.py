from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponse
import json
import datetime
from .forms import OrderForm, CreateUserForm, OrderItemForm, CustomerForm, Order2Form, ProductForm
from .utils import cookieCart, cartData, guestOrder

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import Group
from .decorators import admin_only, user_only

from .filters import OrderFilter

# Create your views here.


@user_only
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

        return redirect('checkout')

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'form': form}
    return render(request, 'food/cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    delivery = request.session['delivery']
    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'delivery': delivery}
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

    if order.take_away == 'Yes':

        return JsonResponse('Payment complete', safe=False)
    else:
        return JsonResponse("payment complete ", safe=False)


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


@admin_only
def dashboard(request):
    orders = Order.objects.all()
    orderitems = OrderItem.objects.all()
    customers = Customer.objects.all()
    products = Product.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(take_away='Yes').count()
    pending = orders.filter(complete='False').count()
    payment = orders.filter(complete='True').count()

    context = {'orders': orders, 'customers': customers, 'orderitems': orderitems, 'products': products, 'payment': payment,
               'total_customers': total_customers, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending}

    return render(request, 'food/dashboard.html', context)


@admin_only
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    orders_count = orders.count()

    orderitems = OrderItem.objects.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'orderitems': orderitems,
               'orders_count': orders_count, 'myFilter': myFilter}
    return render(request, 'food/customer.html', context)


@admin_only
def updateOrder(request, pk_test):
    order = OrderItem.objects.get(id=pk_test)
    form = OrderItemForm(instance=order)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'food/updateorder.html', context)


@admin_only
def cancelOrder(request, pk, pk_test):
    order = Order.objects.get(id=pk)
    orderitem = OrderItem.objects.get(id=pk_test)
    if request.method == 'POST':
        orderitem.delete()
        if request.POST.get('confirm'):
            return redirect('dashboard')

    context = {'order': order, 'orderitem': orderitem}
    return render(request, 'food/cancel_order.html', context)


@admin_only
def customerUpdate(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid:
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'food/customer_update.html', context)


@admin_only
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    orderform = Order2Form(initial={'customer': customer})
    orderitemform = OrderItemForm(initial={'orderform': orderform})

    if request.method == 'POST':
        orderform = Order2Form(request.POST, initial={'customer': customer})
        orderitemform = OrderItemForm(
            request.POST, initial={'orderform': orderform})
        if orderform.is_valid and orderitemform.is_valid:
            order = orderform.save()
            orderitem = orderitemform.save(commit=False)
            orderitem.order = order
            orderitem.save()
            return redirect('dashboard')

    context = {'orderform': orderform, 'orderitemform': orderitemform}
    return render(request, 'food/create_order.html', context)


@admin_only
def addProduct(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'food/add_product.html', context)


@admin_only
def viewProduct(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'food/view_product.html', context)


@admin_only
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid:
            form.save()
            return redirect('view_product')

    context = {'form': form}
    return render(request, 'food/update_product.html', context)


@admin_only
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('view_product')

    context = {'product': product}
    return render(request, 'food/delete_product.html', context)
