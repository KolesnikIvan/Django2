from http.client import PROCESSING
from django.conf import settings
from django.db import models
from mainapp.models import Product
from basketapp.models import Basket

# Create your models here.
class Order(models.Model):
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('-created',)

    CREATED = 'CREATED'
    IN_PROCESSING = 'IN PROCESSING'
    AWAITING_PAYMENT = 'AWAITING_PAYMENT'
    PAID = 'PAID'
    READY = 'READY'
    CANCELLED = 'CANCELLED'
    FINISHED = 'FINISHED'

    ORDER_STATUS_CHOICES = (
        (CREATED, 'created'),
        (IN_PROCESSING, 'in processing'),
        (AWAITING_PAYMENT ,'awaiting payment'),
        (PAID, 'paid'),
        (READY, 'ready'),
        (CANCELLED, 'cancelled'),
        (FINISHED, 'finished'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateField(verbose_name='when was created', auto_now_add=True)
    updated = models.DateField(verbose_name='when was renewed', auto_now=True)
    status = models.CharField(
        verbose_name="order's status", 
        choices=ORDER_STATUS_CHOICES, 
        max_length=20, 
        default=CREATED,
        )
    is_active = models.BooleanField(verbose_name='if the order is active', default=True)

    def __str__(self) -> str:
        return f'Order {self.id}'

    @property
    def items_with_products(self):
        return self.items.select_related('product')

    def get_total_quantity(self):
        # return sum(item.quantity for item in self.items_with_products)
        return sum(item.quantity for item in self.items.all())

    def get_total_cost(self):
        # return sum(item.cost for item in self.items.all())
        # использование мтода cost (внизу) предполагает многократное 
        # обращение к объектам order и product; поэтому
        # select_related returns a QuerySet, that follows foreign-key relationship
        return sum(item.cost for item in self.items.select_related('product'))

    def delete(self):
        for item in self.items.select_related('product'):
            Basket.objects.create(
                user=self.user,
                product=item.product,
                quantity=item.quantity,
                )
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    orders = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity of products', default=0)

    @property
    def cost(self):
        return self.product.price * self.quantity
    