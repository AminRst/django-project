import datetime
import os

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField
# from django_cleanup import cleanup
from django.template.defaultfilters import slugify


# manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    CATEGORY_CHOICES = (
        ('نوشیدنی', 'نوشیدنی'),
        ('فست فود', 'فست فود'),
        ('غذای سنتی', 'غذای سنتی'),
        ('غذای فرنگی', 'غذای فرنگی'),
        ('سایر', 'سایر')
    )

    # relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    # choice field
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='سایر')
    title = models.CharField(max_length=60, blank=True, verbose_name='تیتر پست')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    slug = models.SlugField(max_length=250)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    # data
    publish = models.DateTimeField(default=timezone.now)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    reading_time = models.PositiveIntegerField(verbose_name='زمان مطالعه', blank=True)
    # manager
    objects = models.Manager()
    # objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    name = models.CharField(max_length=250, verbose_name='نام')
    body = models.TextField(verbose_name='متن کامنت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    active = models.BooleanField(default=False, verbose_name='وضعیت')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'{self.name}: {self.post}'


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT / today date/<filename>
#     return '{0}/{1}'.format(datetime.date.today(), filename)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / today date/<filename>
    return '{}/{}'.format(instance.post.author.username, filename)


# @cleanup.select
class Image(models.Model):
    # def user_directory_path(self, filename):
    #     # file will be uploaded to MEDIA_ROOT / post create date/<filename>
    #     x = self.post.create
    #     return '{}/{}'.format((x.year, x.month, x.day), filename)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    # image_file = ResizedImageField(upload_to='post_images', size=[500, 300], crop=['top', 'left'], quality=100)

    image_file = ResizedImageField(upload_to=user_directory_path, size=[500, 300], crop=['top', 'left'], quality=100)

    title = models.CharField(max_length=20, verbose_name='عنوان', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else self.image_file.name

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصویر ها'

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog_account', verbose_name='کاربر')
    date_of_birth = models.DateField(verbose_name='تاریخ تولد', blank=True, null=True)
    bio = models.TextField(verbose_name='بیوگرافی', blank=True, null=True)
    photo = ResizedImageField(verbose_name='تصویر', upload_to='account_images/', size=[500, 500], quality=60,
                              crop=['middle', 'center'], blank='True', null=True)
    job = models.CharField(max_length=250, verbose_name='شعل', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'حساب'
        verbose_name_plural = 'حساب ها'
