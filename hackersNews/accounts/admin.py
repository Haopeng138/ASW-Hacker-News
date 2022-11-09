from django.contrib import admin
from accounts.models import HNUser
# Register your models here.

class Useradmim (admin.ModelAdmin):
    pass

admin.site.register(HNUser,Useradmim)