from django.contrib import admin
from.models import Post,Category
from taggit.admin import TagAdmin

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'views')
    list_filter = ('category', 'author', 'tags')
    search_fields = ('title', 'text')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)