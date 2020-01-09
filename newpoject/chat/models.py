from django.contrib.auth.models import User
from django.db import models
import json
from django.core import serializers

class Messages(models.Model):
    # ממחלקה המייצגת את תכונות ההודעה ומגדירה אותן
    message = models.TextField()
    time = models.CharField(max_length = 20)
    src = models.CharField(max_length = 20)
    dst = models.CharField(max_length = 20)

class UserProfile(models.Model):
    # ממחלקה המייצגת את תכונות המשתמש
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='profiles/')
    friends = models.ManyToManyField("self",blank = True)
    def filter_friends_out(self):
        # פעולה המחזירה רשימה של כל המשתמשים שאין ביניהם קשר חברות
        users_list = UserProfile.objects.exclude(id__in = self.friends.all().values_list('id'))
        return users_list.exclude(id = self.id)

class Chat(models.Model):
    # מחלקה שמאפיינת צ'אט בהתאם לדרישות
    id_chat = models.CharField(max_length = 30)
    messages = models.ManyToManyField(Messages)
    people = models.ManyToManyField(UserProfile)
    def get_messages(self):
        # פעולה ששומרת הודעות לתוך קובץ JSON ושולחת אותה דרך הSOCKET
        messages = self.messages.all()
        data = serializers.serialize('json', messages)
        try:
            data = json.loads(data)
            message_list = [message['fields'] for message in data]
        except IndexError: message_list = []
        return message_list    