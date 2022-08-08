from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Customer(models.Model): #creating the model customer to the db
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True) #This is used when one record of a model A is related to exactly one record of another model B
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
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property #What the @property "decorator" does, is declare that it can be accessed like it's a regular property.

     #This means you can call full_name as if it were a member variable instead of a function, so like this:
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    HOME = [
        ('Yes','Yes'),
        ('No','No'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) #This is used when one record of a model A is related to multiple records of another model B it is many to one field 
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null = True, blank = False)
    transaction_id = models.CharField(max_length=100, null=True)
    take_away = models.CharField(max_length=200, null=True, choices=HOME)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



