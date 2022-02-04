'''
make email unique if not already
'''

from django.db import models
from django.contrib.auth.models import User

'''
The default User model which is imported above comes with 
    Username
    Email
    Password
    roll no
    college name
'''


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional fields.
    #image_upload = models.ImageField(upload_to='user_uploaded_image',blank=True)
    rollno = models.CharField(max_length=16, default='1234567891234567')

    def __str__(self):
        return self.user.username


class MeetingInfo(models.Model):
    topic = models.CharField(max_length=256, blank=True, unique=True)
    sub = models.CharField(max_length=256, blank=True)
    time = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return self.topic
