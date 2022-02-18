from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib import auth
from .models import ShopUser
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from . utils import send_verify_mail

# Create your views here.
def login(request):
    # если приден GET, то строка ниже ничем не инциализирует форму
    if request.method == 'POST': 
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
        
            user = auth.authenticate(request, username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                # user.failed_attempts = 0
                if 'next' in request.GET.keys():
                    return HttpResponseRedirect(request.GET["next"])
                else:
                    return HttpResponseRedirect(reverse('main'))

    else:
        login_form = ShopUserLoginForm()  

    return render(request, 
                'authapp/login.html', 
                context={
                    'title': 'authentification panel',
                    'form': login_form,
                })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user= register_form.save()
            send_verify_mail(user)
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    return render(request, 
                'authapp/register.html', 
                context={
                    'title': 'register you',
                    'form': register_form,
                })


def edit(request):
    # title = 'editing'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)  # PasswordChangeForm(request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('main'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    return render(request, 
                'authapp/register.html', 
                context={
                    'title': 'edit your data',
                    'form': edit_form,
                })


def verify(request, email, activation_key):
    # view to redirect user to verify
    # user = ShopUser.objects.get(email=email)
    user = get_object_or_404(ShopUser, email=email)
    if user.activation_key == activation_key and not user.is_activation_key_expired:
        user.is_active = True
        user.save()
        auth.login(request, user)
    return render(request, 'authapp/verification.html')
    