from django import forms
from django.forms import Textarea

from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش')
    )

    message = forms.CharField(widget=forms.Textarea, required=False)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('شماره تلفن صحیح نیست')
            else:
                return phone

    def clean_message(self):
        message = self.cleaned_data['message']
        if message:
            return message
        else:
            raise forms.ValidationError('فرم پیام خالی است')


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError('نام کوتاه است')
            else:
                return name

    class Meta:
        model = Comment
        fields = ['name', 'body']


# class ContactUsForm(forms.Form):


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'message']

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            return name
        else:
            raise forms.ValidationError('نام و نام خانوادگی را وارد کنید!!!')


class CitiesForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['city']


class SearchForm(forms.Form):
    query = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, required=True)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=250, label='password')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, max_length=250, label='repeat password')

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['first_name', 'last_name', 'email']


class UserEditAccount(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'photo']


class CreateCafeForm(forms.ModelForm):
    image1 = forms.ImageField(label='تصویر اول', required=False)
    image2 = forms.ImageField(label='تصویر دوم', required=False)

    class Meta:
        model = Cafe
        fields = ['name', 'description', 'city', 'address']


# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Cafe
#         fields = ['name', 'description', 'status', 'city', 'address']

# class EditMenu(forms.ModelForm):
#     class Meta:
#         model = Menu
#         fields = ['cafe']

class EditSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']


class EditMenuItemsForm(forms.ModelForm):
    class Meta:
        model = MenuItems
        fields = ['name', 'description', 'price']
