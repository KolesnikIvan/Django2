from django.urls import path, re_path
from . import views

app_name = 'authapp'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    re_path(
        r'^verify/(?P<email>.+)/(?P<activation_key>\w+)', 
        views.verify, 
        name='verify'
        ),
]
