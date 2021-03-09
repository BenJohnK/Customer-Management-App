from django.db import models

# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name
    
    @property
    def orders(self):
        order_count=self.order_set.all().count()
        return order_count

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY=(('Indoor','Indoor'),
              ('Outdoor','Outdoor'),
             )
    name=models.CharField(max_length=200,null=True)
    description=models.CharField(max_length=200,null=True,blank=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    tags=models.ManyToManyField(Tag,null=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS=(('Pending','Pending'),
            ('Out for Delivery','Out for Delivery'),
            ('Delivered','Delivered'),
           )
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    note=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.id)

