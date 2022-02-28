from django import  forms
from authapp.forms import ShopUserEditForm, ShopUserRegisterForm
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser


class ShopUserEditAdminForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'

class ShopUserCreateAdminForm(ShopUserRegisterForm):
    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            # 'password',
            'email',
            'age',
            'avatar',
            'city',
            'phone',
        )

class ProductCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


# class ProductCreateAdminForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'
