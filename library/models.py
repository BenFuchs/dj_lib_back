from django.db import models

# Create your models here.
class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    bName = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    published = models.DateField()
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)

class Loans(models.Model):
    id = models.BigAutoField(primary_key=True)
    UserID = models.IntegerField()
    BookID = models.IntegerField()
    active = models.BooleanField(default=True)
    