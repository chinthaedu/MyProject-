from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_comma_separated_integer_list

# Create your models here.

class User(AbstractUser):
	age=models.IntegerField(default=20)
	mobilenumber=models.CharField(max_length=10,null=True)
	uimg=models.ImageField(upload_to='Profilepics/',default='dummyProfile.png')
	t=[(1,'Guest'),(2,'Manager'),(3,'User')]
	role=models.IntegerField(choices=t,default=1)
	fav=models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, blank=True, null=True,default='')
	rec=models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, blank=True, null=True,default='')
	is_sub=models.IntegerField(default=0)

class Rolereq(models.Model):
	f=[(2,'Manager'),(3,'User')]
	rltype=models.IntegerField(choices=f)
	pfe=models.ImageField(upload_to='Rolereqpics/',default='ab.jpg')
	is_checked=models.BooleanField(default=False)
	uname=models.CharField(max_length=50)
	ud=models.OneToOneField(User,on_delete=models.CASCADE)


class Movie(models.Model):
	moviename=models.CharField(max_length=100)
	album=models.ImageField(upload_to='movieImages/')

	def _str_(self):
		return self.moviename
	
	
class Songs(models.Model):
	songname=models.CharField(max_length=50)
	songno=models.IntegerField(null=True)
	moviename=models.CharField(max_length=50)
	song=models.FileField(upload_to='songs/')
	mv=models.ForeignKey(Movie,on_delete=models.CASCADE)

