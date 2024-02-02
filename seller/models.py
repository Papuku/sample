from django.db import models

# Create your models here.
class Seller(models.Model):
    full_name = models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=30)
    gst = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)


    def __str__(self) -> str:
        return self.full_name



class Product(models.Model):
    product_name=models.CharField(max_length=150)
    dec=models.CharField(max_length=150)
    price=models.DecimalField(max_digits=6, decimal_places=4 ,default=500)
    pic=models.FileField(upload_to='product_images',default='sad_seller.png')
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.product_name



class MyOrder(models.Model):
    all_status = [
        ('pending', 'pending'),
        ('dispatched', 'dispatched')
    ]

    buyer = models.ForeignKey(to='buyer.Buyer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(choices= all_status,max_length=50, default='pending')

    def __str__(self):
        return str(self.id)