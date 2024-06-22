
from django.db import models
class User(models.Model):
    username = models.CharField(max_length=50)
    e_mail = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    filepdf = models.FileField(upload_to='files/')
    rate = models.IntegerField(default=0)
    
    def __str__(self):
        return self.e_mail
    
class Company(models.Model):
    companyname = models.CharField(max_length=50)
    e_mail = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.e_mail
    
class login(models.Model):
    e_mail = models.CharField(max_length=50)
    
    def __str__(self):
        return self.e_mail
    
class Contactus(models.Model):
    Name = models.CharField(max_length=50)
    e_mail = models.CharField(max_length=50)
    Message = models.TextField()
    
class ContactusCom(models.Model):
    Name = models.CharField(max_length=50)
    e_mail = models.CharField(max_length=50)
    Message = models.TextField()
    
class ContactusUser(models.Model):
    Name = models.CharField(max_length=50)
    e_mail = models.CharField(max_length=50)
    Message = models.TextField()
    
class SearchEmployees(models.Model):
    jobtitle = models.CharField(max_length=75)
    e_mail = models.CharField(max_length=50)
    languages = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    experience = models.IntegerField()

class DataOfCV(models.Model):
    text = models.TextField()
    e_mail = models.CharField(max_length=50)
    
    def __str__(self):
        return self.e_mail    
    
class Result(models.Model):
    li_re = models.TextField()