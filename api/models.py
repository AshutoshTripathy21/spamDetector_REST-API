from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=100)

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

class Spam(models.Model):
    number = models.CharField(max_length=15, unique=True)
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE)