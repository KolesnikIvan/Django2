# from django.shortcuts import HttpResponseRedirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from authapp.models import ShopUser
from adminapp.utils import superuser_required
from adminapp.forms import ShopUserEditAdminForm, ShopUserCreateAdminForm
from django.core.paginator import Paginator


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user/edit_u.html'
    form_class = ShopUserCreateAdminForm
    success_url = reverse_lazy("adminapp:users")
    # fields = '__all__'

    @method_decorator(superuser_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'creation of user'
        return context


class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/user/users.html'
    #default tamplate name is modelName_list
    paginate_by = 1
    # pg = Paginator(ShopUser.objects.all())

    @method_decorator(superuser_required)
    def dispatch(self, request, *args, **kwargs):  # http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'list of users'
        return context    


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user/edit_u.html'
    form_class = ShopUserEditAdminForm
    success_url = reverse_lazy("adminapp:users")
    # fields = '__all__'

    @method_decorator(superuser_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get_object(self, queryset):
    #     # return super().get_object(queryset)
    #     return queryset.get(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'user_editing'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user/delete.html'
    success_url = reverse_lazy("adminapp:users")

    def delete(self, request):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete selected user'
        return context
