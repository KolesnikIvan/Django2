from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=100)
    description = models.TextField(verbose_name='описание', blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя', max_length=100)
    price = models.DecimalField(verbose_name='цена', max_digits=7, decimal_places=2, default=0)
    color = models.CharField(verbose_name='цвет', default=0x000000, max_length=20)
    description = models.TextField(verbose_name='описание', blank=True)
    image = models.ImageField(verbose_name='картинка', blank=True, upload_to='products')
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def __str__(self):
        return self.name

