from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Gift(models.Model):
    description = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_url = models.CharField(
        max_length=150, default='http://www.retrofestiveblog.ca/wp-content/uploads/2014/12/badly-wrapped-gift.png')

    def __str__(self):
        return f"{self.description} ({self.id})"

# add a sad gift
# implement photo uploading


# class Comment(models.Model):
#     text = models.CharField(max_length=250)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


# class Like(models.Model):
#     text = models.CharField(max_length=250)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name
