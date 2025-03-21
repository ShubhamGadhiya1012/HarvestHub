# Generated by Django 5.0.6 on 2024-09-19 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HarvestHUB', '0030_userpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpayment',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='userpayment',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
