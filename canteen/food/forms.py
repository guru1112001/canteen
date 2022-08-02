from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['home_delivery']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': ' Enter Name'}),
            'email': forms.TextInput(attrs={'placeholder': ' Enter Email'})
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': ' Enter Password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': ' Confirm Password'})


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['order']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields['name'].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['email'].widget.attrs.update({
                'class': 'form-control'
            })
    
class Order2Form(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields['name'].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['price'].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['category'].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['image'].widget.attrs.update({
                'class': 'form-control'
            })
