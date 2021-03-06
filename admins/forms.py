from django import forms

from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User
from products.models import ProductCategory


class UserAdminRegistrationForm(UserRegistrationForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'age', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': False}))


class CategoryAdminFrom(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    discount = forms.IntegerField(label='Скидка', required=False, min_value=0, max_value=90,
                                  widget=forms.NumberInput(attrs={'class': 'form-control py-4'}))

    class Meta:
        model = ProductCategory
        fields = '__all__'

