from django.contrib import admin

from django.contrib import admin
from .models import Event, Registration

# Register your models so they show up in the admin area
admin.site.register(Event)
admin.site.register(Registration)
