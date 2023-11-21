# Generated by Django 4.2.4 on 2023-09-16 03:40

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_alter_image_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=django_resized.forms.ResizedImageField(crop=['top', 'left'], force_format=None, keep_meta=True, quality=100, scale=None, size=[500, 300], upload_to=blog.models.user_directory_path),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='بیوگرافی')),
                ('photo', django_resized.forms.ResizedImageField(blank='True', crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=60, scale=None, size=[500, 500], upload_to='account_images/', verbose_name='تصویر')),
                ('job', models.CharField(blank=True, max_length=250, null=True, verbose_name='شعل')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'حساب',
                'verbose_name_plural': 'حساب ها',
            },
        ),
    ]
