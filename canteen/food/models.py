from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length = 200, null = True)
    email = models.EmailField(max_length = 200, null = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Todayspl', 'Todays special'),
    )
    p_name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.p_name

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null = True, blank = False)
    transaction_id = models.CharField(max_length=100, null=True)


    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.p_name
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total