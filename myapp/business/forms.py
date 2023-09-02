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

