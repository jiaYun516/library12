from django.contrib import admin
from login.models import identity

# Register your models here.
class identityAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(identity, identityAdmin)