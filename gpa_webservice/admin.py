from django.contrib import admin
from gpa_webservice.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


