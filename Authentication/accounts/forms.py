from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=250)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=250, label='username')
    password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=250, label='password')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, max_length=250, label='repeat password')
    email = forms.CharField(widget=forms.EmailInput, label='email', required=False)

    class Meta:
        model = User
        fields = ['first_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        return cd['username']
