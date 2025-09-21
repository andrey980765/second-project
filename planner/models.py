from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255, blank=True)  # хранит путь внутри static (упрощённо)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.date_time})"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('created', 'Created'),
        ('reminder', 'Reminder'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    notif_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{'✓' if self.seen else '•'}] {self.message}"


# Create your models here.
