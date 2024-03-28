from django.contrib import admin
from .models import Category, Cinema, Comment, Profile

# Register your models here.
class CinemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'views', 'created_at', 'author']
    list_display_links = ['id', 'title']
    list_filter = ['category']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cinema', 'created_at']



admin.site.register(Category)
admin.site.register(Cinema, CinemaAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)
