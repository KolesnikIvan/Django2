"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import authapp
from django.conf import settings
from django.conf.urls.static import static

import mainapp.views as mainapp  # mainapp =import_module('views', 'mainapp')
# from importlib import import_module


urlpatterns = [
    # что делать с этим комментом?
    path('admin/', admin.site.urls),
    path('adminapp/', include('adminapp.urls', namespace='adminapp')),
    path('', mainapp.main, name='main'),
    path('contact/', mainapp.contact, name='contact'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    # path('products/', mainapp.products, name='products'),
    # path('products/<int:pk>', mainapp.category, name='category'), 
]
# path('products/', include('mainapp.urls', namespace='products'))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# menu = Object()

# class Template:
#     header = ...
#     menu = ...
#     content = ...
#     footer = ...

# class ContactTemplate(Template):
#     content = ...

# class ContactTemplate(Template):
#     header = [
#         menu, 
#         # ...
#     ]