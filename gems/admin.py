from django.contrib import admin
from gems.models import Category, Gem, UserProfile, Comment

class GemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'address', 'description', 'image', 'image_source', 'likes', 'reported', 'added_by', 'added_on')
    prepopulated_fields = {'slug':('name',)}
    list_filter = ['reported']
    ordering = ['name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug':('name',)}
    ordering = ['name']
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'gem', 'added_by', 'added_on')
    list_filter = ['gem']
    ordering = ['-added_on']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Gem, GemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)
