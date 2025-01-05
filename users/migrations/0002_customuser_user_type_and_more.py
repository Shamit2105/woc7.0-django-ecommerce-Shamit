# Generated by Django 5.1.4 on 2025-01-05 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('customer', 'Customer'), ('seller', 'Seller')], default='Customer', max_length=12),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='security_question',
            field=models.CharField(choices=[('color', 'What is your favorite color?'), ('food', 'What is your favorite food?'), ('animal', 'What is your favorite animal?'), ('movie', 'What is your favorite movie?'), ('book', 'What is your favorite book?'), ('song', 'What is your favorite song?'), ('tv_show', 'What is your favorite TV show?'), ('game', 'What is your favorite game?'), ('sport', 'What is your favorite sport?'), ('hobby', 'What is your favorite hobby?')], max_length=100),
        ),
    ]
