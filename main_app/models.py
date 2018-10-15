from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Gift(models.Model):
    description = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_url = models.CharField(
        max_length=150, default='http://www.retrofestiveblog.ca/wp-content/uploads/2014/12/badly-wrapped-gift.png')

    def __str__(self):
        return f"{self.description} ({self.id}) @{self.photo_url}"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'id': 1})


# class Photo(models.Model):
#     url = models.CharField(max_length=200)
#     gift = models.ForeignKey(Gift, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Photo for gift_id: {self.gift_id} @{self.url}"
