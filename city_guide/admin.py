from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from city_guide.models import User, Place, Comment, Question

admin.site.register(Place)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(User, UserAdmin)
