import hashlib
# from hashlib import md5
import os
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms as djforms
from .models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser  # form for model shopuser
        fields = ('username', 'password')  # fields of shopuser to use

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        # override to add class
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser  # form for model shopuser
        fields = (
            'username',
            'first_name',
            'password1',
            'password2',
            'email',
            'age',
            'avatar',
            'city',
            'phone',
        )  # fields of shopuser to use

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        # override to add class
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # field.widget.attrs['readonly'] = True

    def save(self):
        user= super().save()
        user.is_active = False
        user.activation_key = hashlib.md5(
            user.email.encode('utf-8') + os.urandom(64)
            ).hexdigest()
        user.save()
        return user

class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            'password',
            'email',
            'age',
            'avatar',
            'city',
            'phone',
        )

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        # override to add class
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = djforms.HiddenInput()

    def clean_city(self):
        # clean - special keyword for method, that must be binded with a validation of the _city field
        city = self.cleaned_data['city']
        if city == 'Kazan':
            raise djforms.ValidationError('No way to Kazan. Stay in Saratov.')
        return city


class ShopUserProfileEditForm(djforms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('about', 'gender')  # 'tagline',

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
