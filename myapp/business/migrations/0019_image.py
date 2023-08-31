# Generated by Django 4.2.4 on 2023-08-22 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0018_alter_cafe_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('photo', models.ImageField(upload_to='pics')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cafe_image', to='business.cafe')),
            ],
        ),
    ]
