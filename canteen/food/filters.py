import django_filters
from django_filters import DateFilter
from .models import *
from django import forms


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_ordered",lookup_expr="gte", label="Order date")
    
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_ordered','transaction_id']
