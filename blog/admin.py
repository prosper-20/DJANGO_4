from django.contrib import admin
from .models import Post, Profile

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "content", 'slug']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "image"]