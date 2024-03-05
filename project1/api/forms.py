from django import forms
from django.contrib.auth.models import User
from .models import User

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    # profile_pic = forms.ImageField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name','address', 'year', 'dob', 'mobile', 'profile_pic']
