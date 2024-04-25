from django.contrib import admin
from .models import Category, Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'views', 'created_at', 'category', 'author']
    list_display_links = ['pk', 'title']
    readonly_fields = ['views']
    list_editable = ['category', 'author']
    list_filter = ['created_at', 'category', 'author']


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
