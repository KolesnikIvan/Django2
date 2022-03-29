import random
from django.core.cache import cache
from django.conf import settings
from functools import cached_property, lru_cache
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Product, ProductCategory
from authapp.models import ShopUser
from django.core.paginator import Paginator, EmptyPage

# вариант кэширования списка продуктов
# список продуктов пересает меняться
def get_products():
    return Product.objects.all()[:4]

# Create your views here.
def main(request):
    # products = Product.objects.all()  # [:4]
    products = get_products()
    user = request.user
    # import pdb; pdb.set_trace()
    return render(request, 'mainapp/index.html',  context ={
        'title': 'Главная',
        'products': products,
        'user':user,
    })

@lru_cache
def get_hot_product(queryset):  #request, pk):
    # return random.choice(Product.objects.all())
    return random.choice(queryset)

def products(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()  # [:4]
    # products = get_products()
    hot_product = get_hot_product(products)

    three_pics = [
        {'adr': 'controll.jpg',},
        {'adr': 'controll1.jpg',},
        {'adr': 'controll2.jpg',},
    ]
    return render(request, 'mainapp/products.html',  context ={
        'title': 'Продукты',
        'pics': three_pics,
        'categories': categories,
        'products': products.exclude(pk=hot_product.pk),  # [:4]
        'hot_product': hot_product,
    })

@lru_cache
def get_prods(category_id):
    return Product.objects.filter(category_id=category_id)

def get_categories():
    # cache.get
    # cache.set
    if settings.LOW_CACHE:
        KEY = 'all_categories'
        categories = cache.get(KEY)
        if not categories:
            categories = ProductCategory.objects.all()
            cache.set(KEY, categories)
        return categories
    else:
        return ProductCategory.objects.all()

def category(request, category_id, page=1):
    # return products(request)
    # category = ProductCategory.objects().get(pk=pk)  # current category
    # categories = ProductCategory.objects.all()       # all categories
    categories = get_categories()
    category = get_object_or_404(ProductCategory, pk=category_id)
    # products = Product.objects.filter(category=category)
    products = get_prods(category_id)
    hot_product = get_hot_product(products)
    
    paginator = Paginator(products.exclude(pk=hot_product.pk), 3)
    try:
        products_page = paginator.page(page)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    return render(
        request,
        "mainapp/products.html",
        context={
            "title": 'Prods', 
            'paginator': paginator,
            'page': products_page,
            # "products": paginator,# products.exclude(pk=hot_product.pk),  # [:4]
            "products": products_page,# products.exclude(pk=hot_product.pk),  # [:4]
            "categories": categories,
            'hot_product': hot_product,  # get_hot_product(products),
            'category':category,
        },
    )


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = ProductCategory.objects.all()
    
    return render(
        request,
        'mainapp/product.html',
        context={
            'title': product.name,
            'product': product,
            'categories': categories,
        }
    )
    # return render(request, 'mainapp/product.html', context={
    #     'pk':pk,
    # })

# @cache_page(None)
def contact(request):
    return render(request, 'mainapp/contact.html',  context ={
        'title': 'Контакты',
    })
