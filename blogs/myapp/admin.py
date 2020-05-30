from django.contrib import admin
from .models import UserProfile,Blog,BlogComment
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Blog)
admin.site.register(BlogComment)
