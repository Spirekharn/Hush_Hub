from django.db import models
from django.conf import settings
# Create your models here.
class Therapist(models.Model):
    name = models.CharField(max_length=255)
    #profile_picture = models.ImageField()
    specialty = models.CharField(max_length=255)
    contact_email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.specialty})"



class AnonymousPost(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='anonymous_posts'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by User {self.user.id} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-timestamp']




class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    appointment_date_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} booked {self.therapist.name} on {self.appointment_date_time}"