from django import forms
from .models import Comment


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش')
    )

    message = forms.CharField(widget=forms.Textarea, required=True)
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
    class Meta:
        model = Comment
        fields = ['name', 'body']