# Generated by Django 5.0.6 on 2024-08-24 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HarvestHUB', '0013_alter_adminpayment_product_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminpayment',
            name='product_order_id',
        ),
    ]
