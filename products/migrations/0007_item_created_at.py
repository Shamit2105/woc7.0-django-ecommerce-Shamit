# Generated by Django 5.1.4 on 2025-01-13 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_item_rating_item_review_author_item_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
