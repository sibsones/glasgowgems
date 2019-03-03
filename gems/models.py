from django.db import models


#superuser
#gemsadmin
#lb05teama

#user model
class User(models.Model):
	username = models.CharField(max_length=30, unique=True, blank=False)
	password = models.CharField(max_length=30)
	emailAddress = models.EmailField(max_length=30)
	profileImage = models.ImageField(upload_to="profile_images/")
	
	def __str__(self):
		return self.name

		
		
#Categoery models
class Category(models.Model):
	name = models.CharField(max_length=30, unique=True, blank=False)
	description = models.CharField(max_length=200)
	slug = models.SlugField(max_length=50)
	
	class Meta:
		verbose_name_plural = 'Categories'
	
	def __str__(self):
		return self.name


		
#'piece of architecture' model
class Page(models.Model):
	name = models.CharField(max_length=99)
	category = models.ForeignKey(Category)
	address = models.CharField(max_length=99)
	description = models.CharField(max_length=200)
	image = models.ImageField(upload_to="page_images/")
	imageSource = models.CharField(max_length=99)
	likes = models.IntegerField(default=0)
	reported = models.BooleanField(default=False)
	addedBy = models.ForeignKey(User)
	addedOn = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(max_length=50)
	
	def __str__(self):
		return self.name
		

		
#commment model
class Comment(models.Model):
	text = models.CharField(max_length=300)
	addedBy = models.ForeignKey(User)
	addedOn = models.DateTimeField(auto_now_add=True)
	page = models.CharField(max_length=50)
	
	def __str__(self):
		return self.name
		
		