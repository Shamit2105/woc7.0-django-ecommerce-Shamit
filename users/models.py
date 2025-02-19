from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phno = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    questions = [
        ('color', 'What is your favorite color?'),
        ('food', 'What is your favorite food?'),
        ('animal', 'What is your favorite animal?'),
        ('movie', 'What is your favorite movie?'),
        ('book', 'What is your favorite book?'),
        ('song', 'What is your favorite song?'),
        ('tv_show', 'What is your favorite TV show?'),
        ('game', 'What is your favorite game?'),
        ('sport', 'What is your favorite sport?'),
        ('hobby', 'What is your favorite hobby?')
    ]
    types = [
        ('customer','Customer'),
        ('seller',"Seller")
    ]
    user_type = models.CharField(max_length=12,choices=types,default='Customer')
    security_question = models.CharField(max_length=100, choices=questions)
    security_answer = models.CharField(max_length=100)
    REQUIRED_FIELDS = ['email', 'security_question', 'security_answer','first_name','last_name','phno','country','state']


