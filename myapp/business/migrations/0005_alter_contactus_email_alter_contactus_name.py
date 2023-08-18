# Generated by Django 4.2.3 on 2023-08-02 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_remove_comment_post_comment_cafe_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='ایمیل آدرس'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='name',
            field=models.CharField(max_length=250, verbose_name='نام و نام خانوادگی'),
        ),
    ]
