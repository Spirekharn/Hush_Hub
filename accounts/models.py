from django.db import models
from django.contrib.auth.models import User

class DailyAffirmation(models.Model):
    text = models.TextField()
    def __str__(self):
        return self.text[:50]

class DailyAffirmationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    affirmation = models.ForeignKey(DailyAffirmation, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.affirmation.text[:20]}"

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.name} for {self.user.username}"