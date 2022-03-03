from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory
from adminapp.forms import ProductCategoryAdminForm
from django.http.response import HttpResponseRedirect
from django.urls import reverse

def category_create(request):
    if request.method == 'POST':
        form = ProductCategoryAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("adminapp:categories"))

    else:
        form = ProductCategoryAdminForm()
    return render(
        request,
        "adminapp/category/edit_c.html",
        context={'title':"create_category", 'form':form},
    )

    
def categories(request):
    categories = ProductCategory.objects.all().order_by('id')  # or .filter()

    return render(request, 'adminapp/category/categories.html', 
        context={
            'title': 'The_categories',
            'objects':categories,
        })

    
def category_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryAdminForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("adminapp:categories"))
    else:
        form = ProductCategoryAdminForm(instance=category)

    return render(
        request, 
        "adminapp/category/edit_c.html", 
        context={'title':"update_category", "form":form},
    )

    
def category_delete(request, pk):
    title = 'category'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        # user.delete()
        # make inactive, not delete
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('admianpp:categories'))
    else:
        content = {'title':title, 'to_delete':category}
        return render(request, 'adminapp/category/delete_c.html', content)
