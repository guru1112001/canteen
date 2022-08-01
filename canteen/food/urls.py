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

    path("dashboard/",views.dashboard,name="dashboard"),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
	path('update_order/<str:pk_test>/', views.updateOrder, name="update_order"),
	path('cancel_order/<int:pk>/<int:pk_test>/', views.cancelOrder, name="cancel_order"),

	path('customer_update/<str:pk>',views.customerUpdate, name="customer_update"),
    path('create_order/<str:pk>', views.createOrder, name="create_order"),

	path('add_product/', views.addProduct, name="add_product"),
	path('view_product/', views.viewProduct, name="view_product"),
	path('update_product/<str:pk>', views.updateProduct, name="update_product"),
	path('delete_product/<str:pk>', views.deleteProduct, name="delete_product"),

]
