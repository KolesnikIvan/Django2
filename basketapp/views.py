from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from mainapp.models import Product
from .models import Basket

# Create your views here.
@login_required
# if request.user.is_authenticatedЖ
    # HttpResponseRedirect('login')  # смысл декоратора
def view(request):
    return render(request, 'basketapp/basket.html', context={
        'title':'The_BASKET',
        'basket': Basket.objects.filter(user=request.user),
    })

@login_required
def add(request, product_id):
    # import pdb; pdb.set_trace()
    product = get_object_or_404(Product, pk=product_id)
    basket_items = Basket.objects.filter(user=request.user, product=product)
    
    if basket_items:
        basket = basket_items[0]  # basket_item.first()
    else:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove(request, basket_item_id):
    basket = get_object_or_404(Basket, pk=basket_item_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def edit_basket(request, basket_item_id, quantity):
    # if request.is_ajax():
        # quantity = int(quantity)
    quantity = quantity
    new_basket_item = Basket.objects.get(pk=int(basket_item_id))
    if quantity > 0:
        new_basket_item.quantity = quantity
        new_basket_item.save()
    else:
        new_basket_item.delete()

    # basket_items = request.user.basket.all().order_by('product__category')
    # basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    # content = {
    #     'basket_items': basket_items,
    # }
    
    # result = render_to_string('basketapp/includes/inc_basket_list.html', content)
    # return JsonResponse({'result': result})
    return render(request, 'basketapp/includes/inc_basket_list.html')  # , content)