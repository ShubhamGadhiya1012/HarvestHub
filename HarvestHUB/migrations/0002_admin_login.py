# Generated by Django 5.0.6 on 2024-07-15 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HarvestHUB', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin_login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
    ]
