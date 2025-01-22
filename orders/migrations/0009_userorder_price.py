# Generated by Django 5.1.4 on 2025-01-22 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_remove_userorder_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
