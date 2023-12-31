# Generated by Django 4.2.4 on 2023-09-26 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0023_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='بیوگرافی')),
                ('photo', django_resized.forms.ResizedImageField(blank='True', crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=60, scale=None, size=[500, 500], upload_to='account_images/', verbose_name='تصویر')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'حساب',
                'verbose_name_plural': 'حساب ها',
            },
        ),
    ]
