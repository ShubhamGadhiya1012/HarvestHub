# Generated by Django 5.0.6 on 2024-08-24 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HarvestHUB', '0017_farmerproduct_razorpay_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerproduct',
            name='razorpay_order_id',
            field=models.CharField(default=False, max_length=100, unique=True),
        ),
    ]
