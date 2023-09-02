# Generated by Django 4.2.4 on 2023-08-24 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0020_delete_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='post_images/')),
                ('title', models.CharField(blank=True, max_length=20, null=True, verbose_name='عنوان')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='business.cafe', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصویر ها',
                'ordering': ['created'],
                'indexes': [models.Index(fields=['created'], name='business_im_created_56cfbb_idx')],
            },
        ),
    ]