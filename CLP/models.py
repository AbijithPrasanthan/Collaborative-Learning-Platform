'''
make email unique if not already
'''

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

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
    time = models.DateTimeField(max_length=6, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self):
        res = {
            'topic': self.topic,
            'sub': self.sub,
            'time': self.time,
            'slug': self.slug,
        }
        return str(res)

class Room(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    username = models.CharField(max_length=1000000, default="Unknown")

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now,blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
