from django.contrib import admin 
from .models import * #imports all models
# Register your models here.

admin.site.register(Customer)#resgister the app or models in admin panel 
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)

