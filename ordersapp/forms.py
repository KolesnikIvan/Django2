from socket import fromshare
from django import forms
from ordersapp.models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # exclude = ('user',)
        fields = []

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        # exclude = (,)
    
    def __inti__(self, *args, **kwargs):
        super(OrderItenForm, *args, **kwargs).__init__()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
