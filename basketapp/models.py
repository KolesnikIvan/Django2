from django.db import models
from django.conf import settings
from mainapp.models import Product

# Create your models here.
class BasketManager(models.Manager):
    # self = Basket.objects
    # in user self = Basket.objects.filter(user=request.user)
    def count(self):
        return len(self.all())

    def total_quantity(self):
        basket_items = self.all()
        return sum(item.quantity for item in basket_items)

        
    def total_cost(self):
        # return sum(len(self.all()[i]) * self.all()[i].price for i in basket)
        #  return sum(self.all()[i].product.price * self.all()[i].quantity for i in len(self.all()))
        basket_items = self.all()
        return sum(item.product.price * item.quantity for item in basket_items)

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
    
    @property
    def cost(self):
        return self.product.price * self.quantity

    # def total_cost(self):
    #     basket_items = self.objects.filter(user=self.user)
    #     return sum(item.product.price * item.quantity for item in basket_items)
    # {% if user.basket|length > 0 %} user.basket[0].total_cost {% end if %}

    def __str__(self):
        return f'{self.product.name} - {self.quantity} pieces.'
