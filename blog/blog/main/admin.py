from django.contrib import admin
from .models import CustomUser, Post, Comment

admin.site.register(CustomUser)


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_image', 'created_at')

    def display_image(self, obj):
        return obj.image.url if obj.image else "No Image"

    display_image.short_description = 'Image'


admin.site.register(Post, PostAdmin)

admin.site.register(Comment)
