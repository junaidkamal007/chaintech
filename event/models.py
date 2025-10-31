from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


class Events(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()    
    location = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return self.title
    
class RSVP(models.Model):
    STATUS_CHOICES = [
        ('Going', 'Going'),
        ('Maybe', 'Maybe'),
        ('Not Going', 'Not Going')
    ]

    event = models.ForeignKey(Events, on_delete=models.CASCADE)   
    user = models.ForeignKey(User, on_delete= models.CASCADE) 
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Going')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - ({self.status})"
    
class Review(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)    

    def __str__(self):
        return f"{self.event.title} - {self.rating}/5"
