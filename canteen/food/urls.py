from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path('breakfast/', views.breakfast, name="breakfast"),
    path('lunch/', views.lunch, name="lunch"),
    path('todayspl/', views.todayspl, name="todayspl"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('register/',views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/',views.logoutUser, name="logout"),

    path('update_item/', views.UpdateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    
]
