from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=100)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='is active', default=True, db_index=True)
    def __str__(self):
        return self.name

class ProductManager(models.Manager):
    def active_items(self):
        return Product.objects.filter(is_active=True)

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя', max_length=100)
    price = models.DecimalField(verbose_name='цена', max_digits=7, decimal_places=2, default=0)
    color = models.CharField(verbose_name='цвет', default=0x000000, max_length=20)
    description = models.TextField(verbose_name='описание', blank=True)
    image = models.ImageField(verbose_name='картинка', blank=True, upload_to='products')
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    is_active = models.BooleanField(verbose_name='active object', default=True)

    objects = ProductManager()

    def __str__(self):
        return self.name


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_on_category_save(
    sender, update_fields, instance, **kwargs
):
    if instance.pk:
        instance.product_set.update(is_active=instance.is_active)
    # instance.product.save()