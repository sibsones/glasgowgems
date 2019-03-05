from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
	name_max_length = 128
	name = models.CharField(max_length=name_max_length, unique=True, blank=False)
	description = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name_plural = 'categories'
	
	def __str__(self):
		return self.name

# Gem = Piece of architecture
class Gem(models.Model):
	name_max_length = 128
	category = models.ForeignKey(Category)
	
	name = models.CharField(max_length=name_max_length, unique=True)
	address = models.CharField(max_length=99)
	description = models.CharField(max_length=200)
	
	image = models.ImageField(upload_to="gems_images")
	image_source = models.CharField(max_length=99)
	
	likes = models.IntegerField(default=0)
	reported = models.BooleanField(default=False)
	
	added_by = models.ForeignKey(User, default=1) ### default=1 for now (1 should be the superuser PK)
	added_on = models.DateTimeField(auto_now_add=True) ### check later if auto_now_add works correctly
	
	slug = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Gem, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.name
		
class Comment(models.Model):
	gem = models.ForeignKey(Gem)
	
	text = models.CharField(max_length=300)
	added_by = models.ForeignKey(User, default=1) ### default=1 for now (1 should be the superuser PK)
	added_on = models.DateTimeField(auto_now_add=True) ### check later if auto_now_add works correctly
	
	def __str__(self):
		return self.text

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    profile_image = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

#===============================================================================
# FOR INFO - DELETE LATER

# Incorrect, User is created automatically by django, just need to link UserProfile to it (at least for now)
# Also, some fields are automatic for User (e.g. username, password, email) so no need to create them explicitly
# 
# user model
# class User(models.Model):
# 	username = models.CharField(max_length=30, unique=True, blank=False)
# 	password = models.CharField(max_length=30)
# 	emailAddress = models.EmailField(max_length=30)
# 	profileImage = models.ImageField(upload_to="profile_images/")
# 	
# 	def __str__(self):
# 		return self.name
#===============================================================================
