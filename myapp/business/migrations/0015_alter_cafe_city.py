# Generated by Django 4.2.4 on 2023-08-16 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0014_cafe_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='city',
            field=models.CharField(choices=[('SH', 'SHIRAZ'), ('NY', 'NEWYORK'), ('MN', 'MANCHESTER')], default='SH', max_length=25),
        ),
    ]
