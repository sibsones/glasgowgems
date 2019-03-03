from django.contrib import admin
from gems.models import User, Category, Page, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Comment)