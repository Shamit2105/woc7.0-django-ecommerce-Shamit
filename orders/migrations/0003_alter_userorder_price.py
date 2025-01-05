# Generated by Django 5.1.4 on 2025-01-05 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_userorder_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
