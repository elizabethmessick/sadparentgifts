from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

# Create your models here.


class Gift(models.Model):
    description = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_url = models.CharField(
        max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} ({self.id}) @{self.photo_url}"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'id': 1})

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    text = models.TextField('Comment', max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment: {self.text}'
