from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from django.forms import inlineformset_factory
from basketapp.models import Basket
from django.db import transaction

# Create your views here.
class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetail(DetailView):
    model = Order

class OrderEditMixin:
    def make_formset(self, instance=None):
        OrderFormSet = inlineformset_factory(Order,
                                    OrderItem,
                                    form=OrderItemForm,
                                    extra=1)
        formset = OrderFormSet(instance=instance)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=instance)
        else:
            if not instance:
                basket_items = self.request.user.basket.all()
                if len(basket_items):
                    OrderFormSet = inlineformset_factory(Order, 
                        OrderItem,
                        form=OrderItemForm,
                        extra=len(basket_items))
                    formset = OrderFormSet()
                    for num, form in enumerate(formset.forms):
                        form.initial['product'] = basket_items[num].product
                        form.initial['quantity'] = basket_items[num].quantity
                        form.initial['price'] = basket_items[num].price
                    basket_items.delete()
        
        self.add_price_to_formset_forms(formset)
        return formset

    def add_price_to_formset_forms(self, formset):
        # add price field to form
        for form in formset.forms:
            if form.instance.pk:
                form.initial['price'] = form.instance.product.price
        return formset

    def save_formset(self, form, formset):  # , instance=None):
        with transaction.atomic():
            # здесь получается пользователь, чтобы показать его в галвной форме
            # а потом проверяется валидность подчиненных форм
            form.instance.user = self.request.user
            self.object = form.save()
            if formset.is_valid():
                # здесь устанавливается связь между заказом и списком его элементов                
                formset.instance = self.object
                formset.save()
            
            # пустой заказ удалить
            # if self.object.get_total_cost() == 0:
            if not self.object.get_total_cost():
                self.object.is_active = False

class OrderCreate(OrderEditMixin, CreateView):
    model = Order
    # import pdb; pdb.set_trace()
    # fields are declared in models.py
    form_class = OrderForm
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderCreate, self).get_context_data(**kwargs)
        data['orderitems'] = self.make_formset()
        return data

    def form_valid(self, form):
        # вызывается после того, как пользователь запостил свои данные в форму
        # вызываю предыдущий метод, получает данные из формы
        context = self.get_context_data()
        orderitems = context['orderitems']

        # import pdb; pdb.set_trace()
        self.save_formset(form, orderitems)
        return super().form_valid(form)

class OrderUpdate(OrderEditMixin, UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('ordersapp:orders_list')
    # fields = '__all__'

    def get_context_data(self, **kwargs):
        data = super(OrderUpdate, self).get_context_data(**kwargs)
        data['orderitems'] = self.make_formset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        self.save_formset(form, orderitems)
        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

def order_forming_complete(request, pk):
    # : replace order status with 'in_processing'
    orders = Order.objects.filter(user=request.user)
    order = get_object_or_404(orders, pk=pk)
    if order.status != Order.CREATED:
        return HttpResponseBadRequest  # error 400, wrong input data
    else:
        order.status = Order.IN_PROCESSING
        order.save()
        return HttpResponseRedirect(reverse('ordersapp:orders_list'))
