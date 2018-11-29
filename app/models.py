# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):

    username= models.ForeignKey(to=User,to_field='username',db_column='username',on_delete=models.CASCADE)
    name= models.TextField(max_length=50)
    dob= models.TextField(max_length=20)
    gender=models.CharField(max_length=1)
    address=models.TextField()
    mobno=models.IntegerField()
    email=models.EmailField( max_length=254)
    course=models.TextField(max_length=50)
    branch=models.TextField(max_length=50)
    cgpa=models.FloatField()
    arrears=models.IntegerField()
    sslc=models.FloatField()
    plustwo=models.FloatField()

    class Meta:
        db_table = 'student'


class Company(models.Model):
    compid=models.IntegerField(primary_key=True)
    compname=models.TextField( max_length=100)
    address=models.TextField()
    contactno=models.IntegerField()
    contactemail=models.EmailField( max_length=254)

    class Meta:
        db_table = 'company'

class job(models.Model):
    jobid=models.IntegerField(primary_key=True)
    compid=models.ForeignKey(to_field='compid',to=Company,on_delete=models.CASCADE)
    jobtype=models.TextField( max_length=100)
    course=models.TextField(max_length=50)
    branch=models.TextField(max_length=50)
    salary=models.IntegerField()
    mincgpa=models.FloatField()
    maxarrears=models.IntegerField()

    class Meta:
        db_table = 'job'

class login(models.Model):
    username=models.TextField(max_length=20)
    password=models.TextField(max_length=50)

    class Meta:
        db_table = 'login'