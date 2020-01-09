from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from . import models
from .models import Messages, UserProfile


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # הפעולה מקבלת את נתוני הלקוח
        # הפעולה מחברת בין השרת ללקוח
        self.group_name = "test"
        self.accept()

    def disconnect(self, close_code):
        # הפעולה מקבלת את נתוני הלקוח
        # הפעולה מנתקת את הקשר בין השרת ללקוח
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,self.channel_name)

    def receive(self, text_data):
        # הפעולה מקבלת את נתוני הלקוח את תוכן הטקסט ששלח השרת ללקוח
        # הפעולה מציגה את תוכן הטקסט ששלח השרת ללקוח
        data = json.loads(text_data)
        def_dict = {
            'get_chat':self.get_chat,
            'new_message':self.new_message
        }
        func = def_dict[data.pop('type')]
        func(data)
        
    def new_message(self,data):   
        # הפעולה מקבלת את נתוני הלקוח ואת תוכן ההודעה
        # הפעולה מציגה ללקוח את תוכן ההודעה החדשה שנכנסה
        # הפעולה עושה הבדלה בין צ'אט אחד לאחר ובודקת האם הצ'אטים הם אותם צ'אטים
        message = models.Messages(**data)
        message.save()
        chat_id = self.group_name
        try:
            chat = models.Chat.objects.get(id_chat = chat_id)
        except:
            chat_id = chat_id.split("Q")
            chat_id = f"{chat_id[1]}Q{chat_id[0]}"
            chat = models.Chat.objects.get(id_chat = chat_id)
        chat.messages.add(message)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,{'type':'send_message',**data})

    def send_message(self, data):
        # מפעיל את הפעולה 'הודעה חדשה' בין כל חברי הקבוצה
        self.send(text_data=json.dumps(data))

    def get_chat(self,data):
        # הפעולה מקבלת את נתוני הלקוח ואת תוכן ההודעות השמורות
        # הפעולה טוענת את הצ'אט בהתאם להיסטוריית ההודעות של צ'אט מסויים
        chat_id = data['chat_id']
        try:
            chat = models.Chat.objects.get(id_chat = chat_id)
        except:
            split_chat_id = chat_id.split("Q")
            chat_id = f"{split_chat_id[1]}Q{split_chat_id[0]}"
            chat = models.Chat.objects.get(id_chat = chat_id)
        self.group_name = chat_id
        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)
        messages = chat.get_messages()
        args = {
            'type': "open_chat",
            'messages':messages
        }
        self.send(text_data=json.dumps(args))