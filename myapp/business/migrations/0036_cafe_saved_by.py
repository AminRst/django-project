# Generated by Django 4.2.4 on 2023-10-22 03:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0035_remove_cafe_like_count_alter_cafe_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='saved_by',
            field=models.ManyToManyField(related_name='saved_cafes', to=settings.AUTH_USER_MODEL),
        ),
    ]