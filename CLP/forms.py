from django import forms
from CLP.models import UserProfileInfo
from django.contrib.auth.models import User

# =========================== REGISTRATION ===========================


class UserProfileInfoForm(forms.ModelForm):
    rollno = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Roll No.'}), label='', required=True)

    class Meta():
        model = UserProfileInfo
        fields = ['rollno']


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Name'}), label='', required=True)

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email'}), label='', required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), label='', required=True)

    class Meta():
        model = User
        fields = ['username', 'email', 'password']

# =========================== FORGOT PASSWORD ===========================


class ResetPassword(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))


'''
confirm password
email verify if from valid college email
    domain verify
    otp send
'''
