from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AnonymousPost, Appointment, Therapist

admin.site.register(AnonymousPost)
admin.site.register(Appointment)
admin.site.register(Therapist)