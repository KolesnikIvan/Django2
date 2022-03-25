from django.shortcuts import render, get_object_or_404
# from adminapp.forms import ProductCreateAdminForm
from mainapp.models import Product, ProductCategory
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from adminapp.utils import superuser_required
from django.urls import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect

# def product_create(request):
#     pass

class ProductCreateView(CreateView):
    model = Product
    # form_class = ProductCreateAdminForm
    template_name = 'adminapp/product/edit.html'
    fields = '__all__'
    # fields = (
    #     'category',
    #     'name',
    #     'price',
    #     'color',
    #     'description',
    #     'image',
    #     'quantity',
    # )

    @method_decorator(superuser_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        return {
            'category':self.get_category(),
        }

    def get_category(self):
        return ProductCategory.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context

    def get_success_url(self):
        return reverse("adminapp:products", kwargs=self.kwargs)


# path('products/read/category/<int:pk>/', adminapp.products, name='products'),
class ProductsAdminView(ListView):
    model = Product
    # cat = ProductCategory.objects.filter(pk=pk)
    # products = Product.objects.filter(category_id=cat) 
    # queryset = get_object_or_404(Product, pk=pk)  
    # cat = get_object_or_404(ProductCategory, pk=pk)
    template_name = 'adminapp/product/products.html'
    
    @method_decorator(superuser_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_category(self):
        return ProductCategory.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'this category products'
        cat = self.get_category(**kwargs)
        context['category'] = self.get_category(**kwargs)
        products = Product.objects.filter(category=cat.pk)
        context['object_list'] = products
        # import pdb; pdb.set_trace()
        return context


@superuser_required
def product_read(request):
    pass
# DetailedView

# path('products/read/<int:pk>/', adminapp.product_read, name='product_read'),
class ProductReadAdminView(DetailView):
    model = Product
    template_name = 'adminapp/product/product.html'
 
    # @method_decorator(superuser_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)
    def get_cotext_data(self, **kwargs):
        # в inc_categories_menu.html не увидел категории товара, а только all
        # поэтому пытаюсь переопределить контекст с передачей ему категории
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all().filter(pk=self.kwargs['pk'])
        return context


# UpdateView
class ProductUpdateAdminView(UpdateView):
    model = Product
    template_name = 'adminapp/product/edit.html'
    fields = '__all__'
    success_url = reverse_lazy('adminapp:products')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['category'] = ProductCategory.objects.get(pk=self.kwargs['pk'])
    #     return context

def product_delete(request, pk):
    pass
# DeleteView

class ProductDeleteAdminView(DeleteView):
    model = Product
    template_name = 'adminapp/product/delete.html'
    success_url = 'adminapp:products'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete prod'
        return context
