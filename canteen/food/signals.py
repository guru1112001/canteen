from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer, Order


def Customer_profile(sender, instance, created, **kwargs):

    if created:      
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )

        print('Profile created')


post_save.connect(Customer_profile, sender=User)
