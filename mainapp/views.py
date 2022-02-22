import random
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def main(request):
    products = Product.objects.all()[:4]
    return render(request, 'mainapp/index.html',  context ={
        'title': 'Главная',
        'products': products,
    })

def get_hot_product(queryset):  #request, pk):
    # return random.choice(Product.objects.all())
    return random.choice(queryset)

def products(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()  # [:4]
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


def category(request, category_id, page=1):
    # return products(request)
    # category = ProductCategory.objects().get(pk=pk)  # current category
    categories = ProductCategory.objects.all()       # all categories
    category = get_object_or_404(ProductCategory, pk=category_id)
    products = Product.objects.filter(category=category)
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


def contact(request):
    return render(request, 'mainapp/contact.html',  context ={
        'title': 'Контакты',
    })
