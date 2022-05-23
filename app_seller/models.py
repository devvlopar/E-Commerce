from django.db import models

# Create your models here.
class Seller(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Products(models.Model):
    pname = models.CharField(max_length=30)
    price = models.FloatField()
    pic = models.FileField(upload_to='products',default='product.png')
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)

    def __str__(self):
        return self.pname