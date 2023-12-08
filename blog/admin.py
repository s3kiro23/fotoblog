from django.contrib import admin
from blog.models import Photo, Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('photo', 'title', 'content', 'date_created', 'starred', 'word_count')


admin.site.register(Blog, BlogAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'caption', 'uploader', 'date_created')


admin.site.register(Photo, PhotoAdmin)
