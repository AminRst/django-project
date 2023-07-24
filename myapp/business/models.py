from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels


# manager
class OpenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Cafe.Status.OPEN)


# Create your models here.
class Cafe(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OP', 'Open'
        CLOSE = 'CL', 'Close'

    # relations
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='costumer_cafe')
    # choice field
    name = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CLOSE)
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
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="comment", verbose_name="پست")
    name = models.CharField(max_length=250, verbose_name="نام")
    body = models.TextField(verbose_name="متن کامنت")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
                   ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'{self.name}: {self.cafe}'

