from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
from . models import Customer

def create_customer(sender,instance,created,**kwargs):
    if created:
        group=Group.objects.get(name="customers")
        instance.groups.add(group)
        Customer.objects.create(user=instance,name=instance,email=instance.email)
post_save.connect(create_customer,sender=User)

def update_customer(sender,instance,created,**kwargs):
    if created==False:
        instance.customer.save()
post_save.connect(update_customer,sender=User)
