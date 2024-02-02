from django.db import models
from seller.models import Product
# Create your models here.


class Buyer(models.Model):
    first_name =models.CharField(max_length=50)
    last_name =models.CharField(max_length=50)
    email =models.EmailField(unique=True)
    password =models.CharField(max_length=20)
    addres=models.TextField(max_length=250)
    mobile=models.CharField(max_length=15)
    pic=models.FileField(upload_to='buyer_profile', default='sad.webp')
    


    def __str__(self) -> str:
        return self.email


class Cart(models.Model):
    product=models.ForeignKey(Product ,on_delete=models.CASCADE)
    buyer=models.ForeignKey(Buyer,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return str(self.buyer)