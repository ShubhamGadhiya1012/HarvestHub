# Generated by Django 5.0.6 on 2024-08-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HarvestHUB', '0025_farmerproduct_razorpay_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerproduct',
            name='razorpay_order_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
