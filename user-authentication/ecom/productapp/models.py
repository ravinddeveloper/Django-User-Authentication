from django.db import models

# Create your models here.

class products(models.Model):
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,default="")
    sub_category=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=500)
    pub_date=models.DateField(auto_now=False, auto_now_add=False)
    image=models.ImageField(upload_to='shop/images', max_length=None,default="") # pip install pillow

    def __str__(self):
        return self.product_name
