from django.db import models

# Create your models here.
class User(models.Model):

    fname = models.CharField(max_length=40) 
    lname = models.CharField(max_length=40)
    email = models.EmailField(unique=True) 
    mobile = models.CharField(max_length=40) 
    password = models.CharField(max_length=40) 
    pic= models.FileField(upload_to='profile',default='abc.png')
    
    def __str__(self):
        return self.fname + ' ' + self.lname 