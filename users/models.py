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
        ('What is your favorite color?','color'),
        ('What is your favorite food?','food'),
        ('What is your favorite animal?','animal'),
        ('What is your favorite movie?','movie'),
        ('What is your favorite book?','book'),
        ('What is your favorite song?','song'),
        ('What is your favorite TV show?','tv_show'),
        ('What is your favorite game?','game'),
        ('What is your favorite sport?','sport'),
        ('What is your favorite hobby?','hobby')
    ]
    security_question = models.CharField(max_length=100, choices=questions)
    security_answer = models.CharField(max_length=100)
    REQUIRED_FIELDS = ['email', 'security_question', 'security_answer','first_name','last_name','phno','country','state']


