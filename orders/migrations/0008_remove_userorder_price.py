# Generated by Django 5.1.4 on 2025-01-22 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userorder',
            name='price',
        ),
    ]
