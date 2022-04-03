from django.contrib import admin
from .models import Post,Comments,Profile,Follow

# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Follow)