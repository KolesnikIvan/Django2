from django.db import models
from django.conf import settings
from mainapp.models import Product
from functools import cached_property, lru_cache

# Create your models here.
class BasketQuerySet(models.query.QuerySet):
    # QuerySet's delete shoukd be overriden, not Manager's
    # https://stackoverflow.com/questions/6459616/overriding-queryset-delete-in-django
    def delete(self, *args, **kwargs):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super().delete(*args, **kwargs)


class BasketManager(models.Manager):
    # self = Basket.objects
    # in user self = Basket.objects.filter(user=request.user)
    # Manager is the object that provied database query operations to Django models
    
    def count(self):
        return len(self.all())

    # @cached_property
    @lru_cache
    def total_quantity(self):
        basket_items = self.all()
        return sum(item.quantity for item in basket_items)

    # @cached_property
    @lru_cache    
    def total_cost(self):
        # return sum(len(self.all()[i]) * self.all()[i].price for i in basket)
        #  return sum(self.all()[i].product.price * self.all()[i].quantity for i in len(self.all()))
        basket_items = self.all()
        return sum(item.product.price * item.quantity for item in basket_items)

    def get_queryset(self):
        return BasketQuerySet(self.model, using=self.db)


class Basket(models.Model):
    class Meta:
        # ordering = ('-quantity',)
        ordering = ('id',)
        unique_together = ['user', 'product']
        
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE, related_name='basket')
    # product = models.ForeignKey(Product, unique=True, on_delete=models.CASCADE)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    # product = models.OneToOneField(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity of goods', default=0)
    add_datetime = models.DateTimeField(verbose_name='time', auto_now_add=True)

    objects = BasketManager()
    
    def save(self, *args, **kwargs):
        # при сохранении товара в корзине соответственно уменьшить остаток
        if self.pk:
            # сколько стало минус сколько было
            old_basket = Basket.objects.get(pk=self.pk)
            self.product.quantity -= self.quantity - old_basket.quantity
        else:
            self.product.quantity -= self.quantity
        # import pdb; pdb.set_trace()
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # при удалении товара из корзины, его надо прибавить к остатку
        self.product.quantity += self.quantity
        # import pdb; pdb.set_trace()
        self.product.save()
        super().delete(*args, **kwargs)

    @property
    def cost(self):
        return self.product.price * self.quantity

    # def total_cost(self):
    #     basket_items = self.objects.filter(user=self.user)
    #     return sum(item.product.price * item.quantity for item in basket_items)
    # {% if user.basket|length > 0 %} user.basket[0].total_cost {% end if %}

    def __str__(self):
        return f'{self.product.name} - {self.quantity} pieces.'
