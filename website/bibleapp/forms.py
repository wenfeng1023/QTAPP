from pyexpat import model
from random import choices
from secrets import choice
from django import forms
from .models import User_Profile,DateSave
from django.contrib.auth.models import User
from .models import User_Profile,My_Meditation,Prayer
from django.utils.safestring import mark_safe

class UpdateUserProfileForm(forms.ModelForm):

    nickname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    phoneNo = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    self_introduce = forms.CharField(required=False,widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))

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
class MyMeditationForm(forms.ModelForm):
    # owner = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
    #     'class': 'form-control', 'readonly': 'readonly','cols': 80
    # }))
    scripture = forms.CharField(widget= forms.Textarea(attrs={
        'class': 'form-control'
    }))
    text=forms.CharField(widget= forms.Textarea(attrs={
        'class': 'form-control'
    }))
    choice= [('1','공개'),('2','비공개')]
    choice = forms.CharField(widget=forms.RadioSelect(choices=choice)
       )
    

    class Meta:
        model = My_Meditation
        fields = ['text','scripture','choice']

class PrayerForm(forms.ModelForm):
    # owner = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
    #     'class': 'form-control', 'readonly': 'readonly','cols': 80
    # }))
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control'}))
    text=forms.CharField(widget= forms.Textarea(attrs={
        'class': 'form-control'
    }))
    choice= [('1','공개'),('2','비공개')]
    choice = forms.CharField(widget=forms.RadioSelect(choices=choice)
       )
    

    class Meta:
        model = Prayer
        fields = ['title','text','choice']


class DateSaveForm(forms.Form):
    date = forms.DateField(label='日期', widget=forms.DateInput(attrs={'type':'date'}))
