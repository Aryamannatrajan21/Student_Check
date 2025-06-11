from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_TYPES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
