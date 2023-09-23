from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ConverseNetUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=50)
    Date_Of_Birth = models.DateField(null=True)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Profile(models.Model):
    converseNet_user = models.ForeignKey(ConverseNetUser, on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=10000000)


class Bot_Message(models.Model):
    converseNet_user = models.ForeignKey(ConverseNetUser, on_delete=models.CASCADE, null=True)
    converseNet_user_Message = models.TextField(max_length=10000000, default=None)
    reply_Message = models.TextField(max_length=10000000)
    message_Time = models.DateTimeField(default=datetime.now, blank=True)


class Diary(models.Model):
    title = models.CharField(max_length=500)
    converseNet_user = models.ForeignKey(ConverseNetUser, on_delete=models.CASCADE, null=True)
    note = models.TextField(max_length=10000000, default=None)
    time = models.DateTimeField(default=datetime.now, blank=True)


class FriendsThread(models.Model):
    friends_User_id_Person1 = models.ForeignKey(ConverseNetUser, on_delete=models.CASCADE, null=True,
                                                related_name='person1')
    friends_User_id_Person2 = models.ForeignKey(ConverseNetUser, on_delete=models.CASCADE, null=True)


class Requests(models.Model):
    friends_User_id_Person1 = models.ForeignKey(ConverseNetUser, on_delete=models.CASCADE, null=True,
                                                related_name='person12')
    friends_User_id_Person2 = models.ForeignKey(ConverseNetUser, on_delete=models.CASCADE, null=True)
    status = models.TextField(max_length=1000000)


class FriendsThreadMessage(models.Model):
    message = models.TextField(max_length=1000000)
    friends_Chat_Time = models.DateTimeField(default=datetime.now, blank=True)
    sender_Id = models.ForeignKey(ConverseNetUser, on_delete=models.CASCADE, null=True)
    thread_Id = models.ForeignKey(FriendsThread, on_delete=models.CASCADE, null=True, related_name='Thread')
