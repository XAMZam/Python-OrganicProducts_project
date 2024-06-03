# Generated by Django 5.0.6 on 2024-05-24 03:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_product_images_product_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.RemoveField(
            model_name='product',
            name='prices',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='weight',
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='Your default description here'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='path/to/default/image/default.jpg', upload_to='path/to/default/image/'),
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default='Default Name', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
