# Generated by Django 5.0.6 on 2024-07-15 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HarvestHUB', '0002_admin_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=255)),
            ],
        ),
    ]
