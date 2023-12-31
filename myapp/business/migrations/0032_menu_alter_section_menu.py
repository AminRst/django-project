# Generated by Django 4.2.4 on 2023-10-08 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0031_alter_section_menu_delete_menu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('cafe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='business.cafe', verbose_name='کافه')),
            ],
            options={
                'verbose_name': 'منو',
                'verbose_name_plural': 'منو ها',
            },
        ),
        migrations.AlterField(
            model_name='section',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='business.menu'),
        ),
    ]
