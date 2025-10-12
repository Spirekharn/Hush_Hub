from django.contrib import admin
from .models import DailyAffirmation, DailyAffirmationLog, EmergencyContact

admin.site.register(DailyAffirmation)
admin.site.register(DailyAffirmationLog)
admin.site.register(EmergencyContact)