from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=30, unique=True, blank=False)
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
	category = models.ForeignKey(Category)
	
	name = models.CharField(max_length=99, unique=True)
	address = models.CharField(max_length=99)
	description = models.CharField(max_length=200)
	
	image = models.ImageField(upload_to="gems_images")
	image_source = models.CharField(max_length=99)
	
	latitude = models.DecimalField(max_digits=22, decimal_places=16, default=-1000)
	longitude = models.DecimalField(max_digits=22, decimal_places=16, default=-1000)
	
	likes = models.IntegerField(default=0)
	reported = models.BooleanField(default=False)
	
	### default=1 should be the superuser PK, changed correctly when adding a gem
	added_by = models.ForeignKey(User, default=1)
	### auto_now_add works correctly, auto assigns date and time when adding a gem
	added_on = models.DateTimeField(auto_now_add=True)
	
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
