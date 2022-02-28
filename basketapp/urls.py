from django.urls import path
from . import views

app_name = 'basketapp'

urlpatterns = [
    path('', views.view, name='view'),
    path('add/<int:product_id>', views.add, name='add'),
    path('remove/<int:basket_item_id>/', views.remove, name='remove'),
    path('edit/<int:basket_item_id>/<int:quantity>/', views.edit_basket, name='edit'),
]
