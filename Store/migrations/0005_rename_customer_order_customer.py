# Generated by Django 5.0.6 on 2024-06-03 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_rename_product_orderitem_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Customer',
            new_name='customer',
        ),
    ]