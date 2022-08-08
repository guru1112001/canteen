from django.forms import ModelForm  #Django ModelForm is a class that is used to directly convert a model into a Django form
from django.contrib.auth.forms import UserCreationForm #Django UserCreationForm is used for creating a new user that can use our web application.
from django import forms
from .models import *
from django.contrib.auth.models import User # Django comes with a user authentication system. and it is used for authentication

class OrderForm(ModelForm):
    class Meta:# Model Meta is basically used to change the behavior of your model fields 
        model = Order
        fields = ['take_away']

class CreateUserForm(UserCreationForm):# this class create the user so customer can the access the site 
    
    class Meta:
        model = User
        fields = ["first_name",'username','email','password1','password2'] #fields which we wants in registeration form 
        widgets = { #widgets to edit the fields in a particular way
            "first_name": forms.TimeInput(attrs={"placeholder": "enter your Name "}),
            'username': forms.TextInput(attrs={'placeholder': ' Enter UserName'}),
            'email': forms.TextInput(attrs={'placeholder': ' Enter Email'}),
    
        }

    def __init__(self, *args, **kwargs): #contructor of a class 
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': ' Enter Password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': ' Confirm Password'})

#all these  class is inherirate by modelform class which convert models into forms
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
