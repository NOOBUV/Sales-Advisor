from django.contrib import admin
from .models import Organization, User, Database

# Register your models here.
admin.site.register(Organization)
admin.site.register(User)
admin.site.register(Database)