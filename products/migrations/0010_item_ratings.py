# Generated by Django 5.1.4 on 2025-01-16 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_subcategories_subcategory_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='ratings',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
    ]
