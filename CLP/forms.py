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
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}), label='', required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password','password1']

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password1')
        if password1 != password2:
            self._errors['password1'] = self.error_class(['Password Does Not Matched'])


# =========================== FORGOT PASSWORD ===========================



class ResetPassword(forms.Form):
    Email = forms.EmailField()
    def __str__(self):
        return self.Email


'''
confirm password
email verify if from valid college email
    domain verify
    otp send
'''
