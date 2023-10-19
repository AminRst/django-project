# Generated by Django 4.2.4 on 2023-10-19 03:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0034_remove_menuitems_cafe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafe',
            name='like_count',
        ),
        migrations.AlterField(
            model_name='cafe',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]