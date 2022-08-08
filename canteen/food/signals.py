from django.db.models.signals import post_save #post save "save the object at that time"
from django.contrib.auth.models import User
from .models import Customer, Order
# this function send a signals whenever your is created 
#  instance is the actual object that has just been saved and triggered the post_save signal

def Customer_profile(sender, instance, created, **kwargs):

    if created:      
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )

        


post_save.connect(Customer_profile, sender=User)
