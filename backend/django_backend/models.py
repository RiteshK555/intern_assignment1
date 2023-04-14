from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=255)
    data = models.TextField()
    date_time = models.DateTimeField()
    location =  models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

