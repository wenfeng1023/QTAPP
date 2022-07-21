from django import forms
from .models import User_Profile
from django.contrib.auth.models import User
from .models import User_Profile


class UpdateUserProfileForm(forms.ModelForm):

    nickname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    phoneNo = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    self_introduce = forms.Textarea(attrs={
        'class': 'form-control'
    })

    profile_img = forms.ImageField(required=False, widget=forms.FileInput)



    class Meta:
        model = User_Profile
        fields = ['nickname', 'phoneNo', 'self_introduce', 'profile_img']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'readonly': 'readonly'
    }))

    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'readonly': 'readonly'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
