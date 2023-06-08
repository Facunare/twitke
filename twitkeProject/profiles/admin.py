from django.contrib import admin
from .models import Profiles, verfifyRequests, unbanRequests
# Register your models here.
admin.site.register(Profiles)
admin.site.register(verfifyRequests)
admin.site.register(unbanRequests)