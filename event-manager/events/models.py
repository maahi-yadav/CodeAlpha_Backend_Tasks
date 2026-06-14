from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)       # <-- Fixed max_length here!
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)    # <-- Fixed max_length here!

    def __str__(self):
        return self.title

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)   # <-- Fixed max_length here!
    user_email = models.EmailField()
    registration_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.user_name} - {self.event.title}"