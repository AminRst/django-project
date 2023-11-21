from django import forms
from .models import Comment, Post, Account
from django.contrib.auth.models import User


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("پیشنهاد", "پیشنهاد"),
        ("انتقاد", "انتقاد"),
        ("گزارش", "گزارش")
    )
    subject = forms.CharField()
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('شماره تلفن صحیح نیست')
            else:
                return phone

    def clean_message(self):
        message = self.cleaned_data['message']
        if not message:
            raise forms.ValidationError('متن پیام را وارد کنید!')
        else:
            return message


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


class NewPostForm(forms.ModelForm):

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            if 3 < len(title) < 60:
                return title
            else:
                raise forms.ValidationError('تیتیر باید بیشتر از 3 و کمتر 60 کاراکتر باشد')
        else:
            raise forms.ValidationError('تیتر پست را واد کنید')

    def clean_reading_time(self):
        reading_time = self.cleaned_data['reading_time']
        if reading_time:
            if reading_time > 0:
                return reading_time
            else:
                raise forms.ValidationError('مدت زمان مورد نیاز برای مطالعه باید بزرگتر از صفر باشد')
        else:
            raise forms.ValidationError(' مدت زمان مورد نیاز برای مطالعه را وارد کنید')

    def clean_description(self):
        description = self.cleaned_data['description']
        if description:
            if len(description) > 10:
                return description
            else:
                raise forms.ValidationError('توضیحات باید بیشتر از 10 کاراکتر باشد')
        else:
            raise forms.ValidationError(' توضیحات پست را وارد کنید')

    class Meta:
        model = Post
        fields = ['title', 'reading_time', 'description']

        # fields = ['author', 'title', 'reading_time', 'description']
        # widgets = {
        # 'author': forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'request.user'})
        # }


class SearchForm(forms.Form):
    query = forms.CharField()


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label='تصویر اول')
    image2 = forms.ImageField(label='تصویر دوم')

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time', 'category']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=250)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=250, label='password')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, max_length=250, label='repeat password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserEditAccount(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'job', 'photo', 'bio']
