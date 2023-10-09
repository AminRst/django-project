from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# from django_jalali.db import models as jmodels
from django_resized import ResizedImageField


# manager
class OpenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Cafe.Status.OPEN)


# Create your models here.
class Cafe(models.Model):
    class Cities(models.TextChoices):
        SHIRAZ = 'SH', 'SHIRAZ'
        NEWYORK = 'NY', 'NEWYORK'
        MANCHESTER = 'MN', 'MANCHESTER'

    class Status(models.TextChoices):
        OPEN = 'OP', 'Open'
        CLOSE = 'CL', 'Close'

    image_caption = models.CharField(max_length=100, default='Photo by Blog')
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')

    # relations
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='costumer_cafe')
    # choice field
    name = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CLOSE)
    city = models.CharField(max_length=25, choices=Cities.choices, default=Cities.SHIRAZ)
    address = models.CharField(max_length=100)
    # data
    publish = models.DateTimeField(default=timezone.now)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    # manager
    objects = models.Manager()
    opened = OpenManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = 'کافه'
        verbose_name_plural = 'کافه ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('business:cafe_detail', args=[self.id])


class Ticket(models.Model):
    message = models.TextField(verbose_name='پیام')
    name = models.CharField(max_length=250, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    subject = models.CharField(max_length=250, verbose_name='موضوع')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return self.subject


class Comment(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="comments", verbose_name="کافه")
    name = models.CharField(max_length=250, verbose_name="نام")
    body = models.TextField(verbose_name="متن کامنت")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    # email = models.EmailField(verbose_name="ایمیل")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'{self.name}: {self.cafe}'


class ContactUs(models.Model):
    name = models.CharField(blank=True, max_length=250, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل آدرس')
    subject = models.CharField(max_length=250, verbose_name='موضوع', default='')
    message = models.TextField(verbose_name='متن پیام')

    class Meta:
        verbose_name = 'پیام های کاربر'
        verbose_name_plural = 'پیام های کاربران'

    def __str__(self):
        return f'{self.name}'


class Image(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='images', verbose_name='تصویر')
    image_file = models.ImageField(upload_to='cafe_images/')
    title = models.CharField(max_length=20, verbose_name='عنوان', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else 'None'

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصویر ها'


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account', verbose_name='کاربر')
    date_of_birth = models.DateField(verbose_name='تاریخ تولد', blank=True, null=True)
    bio = models.TextField(verbose_name='بیوگرافی', blank=True, null=True)
    photo = ResizedImageField(verbose_name='تصویر', upload_to='account_images/', size=[500, 500], quality=60,
                              crop=['middle', 'center'], blank='True', null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'حساب'
        verbose_name_plural = 'حساب ها'


class Like(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'


class Menu(models.Model):
    cafe = models.OneToOneField(Cafe, on_delete=models.CASCADE, primary_key=True, verbose_name="کافه")

    class Meta:
        verbose_name = 'منو'
        verbose_name_plural = 'منو ها'

    def __str__(self):
        return self.cafe.name


class Section(models.Model):
    name = models.CharField(max_length=50, verbose_name='دسته')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='sections')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name


class MenuItems(models.Model):
    cafe = models.CharField(max_length=50, verbose_name='نام کافه', default=None, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='دسته بندی', related_name='section')
    name = models.CharField(max_length=50, verbose_name='نام')
    description = models.CharField(max_length=250, verbose_name='توضیحات', default=None, blank=True)
    price = models.FloatField(verbose_name='قیمت')

    class Meta:
        verbose_name = 'گزینه منو'
        verbose_name_plural = 'گزینه های منو'

    def __str__(self):
        return self.name
