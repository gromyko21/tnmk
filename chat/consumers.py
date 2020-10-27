from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Count
from django.utils.safestring import mark_safe
import re


User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        chat_id = get_object_or_404(Chat, id=self.room_name)
        messages = Message.objects.order_by('-pk').filter(recipient=chat_id)[:5]
        count = Chat.objects.filter(id=self.room_name).annotate(Count('members'))
        count = count[0].members__count
        messages.count = count
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        room_name = data['room_name']
        author_user = User.objects.filter(username=author)[0]

        chat = Chat.objects.get(id=room_name)
        try:
            file_message = data['file']
            message = Message.objects.create(
                author=author_user,
                content=data['message'],
                file=file_message,
                recipient=chat
            )
        except KeyError:
            try:
                image_message = data['image']
                # image_message = re.split(r'/media/', image_message)[1:]
                # print(image_message)
                message = Message.objects.create(
                    author=author_user,
                    content=data['message'],
                    image=image_message,
                    recipient=chat
                )
            except KeyError:
                message = Message.objects.create(
                    author=author_user,
                    content=data['message'],
                    image='',
                    recipient=chat
                    )
        users = chat.members.all()
        for user in users:
            new_data = ReadMessage.objects.create(room_id=room_name, recipient=user.id, message_id=message.id)
            new_data.save()
        # print(new_data)

        message1 = Message.objects.order_by('-pk').filter(recipient=chat)[0:1]

        count = Chat.objects.filter(id=room_name).annotate(Count('members'))
        count = count[0].members__count
        chat.count = count
        chat.message = message1

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        read = '1'
        count_members = len(message.recipient.members.all())
        if count_members == 2:
            data_chats = {
                'author': message.author.username,
                'first_name': message.author.profile.first_name + ' ' + message.author.profile.last_name,
                'image': message.author.profile.image.url,
                'id': message.author.profile.id,
                'slug': message.author.profile.slug,
                'content': message.content,
                'image_message': message.image,
                'file_message': message.file,
                # 'image_message': mark_safe(json.dumps(str(message.image_message))),
                'read_message': read,
                'room_id': message.recipient.id,
                'timestamp': str(message.timestamp)[:16],
            }

        else:
            data_chats = {
                'test': 'test',
                'author': message.author.username,
                'first_name': message.author.profile.first_name + ' ' + message.author.profile.last_name,
                'image': message.author.profile.image.url,
                'id': message.author.profile.id,
                'slug': message.author.profile.slug,
                'content': message.content,
                'image_message': message.image,
                'file_message': message.file,
                'read_message': read,
                'room_id': message.recipient.id,
                'timestamp': str(message.timestamp)[:16],

                'author1': message.author.username,
                'first_name1': message.recipient.group_name,
                'image1': message.recipient.image_chat.url,
                'id1': message.author.profile.id,
                'slug1': message.author.profile.slug,
                'content1': message.content,
                'image_message1': message.image,
                'read_message1': read,
                'room_id1': message.recipient.id,
                'timestamp1': str(message.timestamp)[:16],
            }
        return data_chats

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        body_chat = Chat.objects.filter(id=self.room_name)
        body_chat = body_chat[0].members.all()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        body_chat = Chat.objects.order_by('-pk').filter(id=self.room_name)
        body_chat = body_chat[0].members.all()

        for user in body_chat:
            async_to_sync(self.channel_layer.group_send)(
                'user_%s' % user.id,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))


class AllChatsConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        pass
        # # messages = Chat.objects.order_by('received_messages__timestamp')#.filter(members=self.scope['user'])
        #
        # for chat in messages:
        #     chat_id = get_object_or_404(Chat, id=chat.id)
        #     message = Message.objects.order_by('-pk').filter(recipient=chat_id)[0:1]
        #     chat.message = message
        #     # Получаем количество получателей в комнате
        #     # Чтобы решить личный чат это или беседа
        #     count = Chat.objects.filter(id=chat_id.id).annotate(Count('members'))
        #     count = count[0].members__count
        #     chat.count = count
        #
        # content = {
        #     'command': 'messages',
        #     'messages': self.messages_to_json(messages)
        # }
        # self.send_message(content)

    def new_message(self, data):
        author = data['from']
        room_name = data['room_name']
        author_user = User.objects.filter(username=author)[0]

        chat = Chat.objects.get(id=room_name)
        chat_id = get_object_or_404(Chat, id=room_name)
        message1 = Message.objects.order_by('-pk').filter(recipient=chat_id)[0:1]

        count = Chat.objects.filter(id=room_name).annotate(Count('members'))
        count = count[0].members__count
        chat.count = count
        chat.message = message1

        content = {
            'command': 'new_message',
            'message': self.message_to_json(chat)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        # Проверка непрочитанных сообщений
        read = ''
        # you = 'Вы:'
        if message.message[0].author:
            if self.scope['user'] != message.message[0].author:
                if message.message[0].is_readed == False:
                    you = message.message[0].author.profile.first_name + ': '
                    read = 1


        # Проверка на загрузку фоторгафии и имени пользователя в личной беседе
        if self.scope['user'] == message.members.all()[0]:
            data_message = {
                'first_name': message.members.all()[1].profile.first_name + ' ' + message.members.all()[1].profile.last_name,
                'image': message.members.all()[1].profile.image.url,
                'slug': message.members.all()[1].profile.slug,
                'id': message.members.all()[1].profile.id,
                'room_id': message.id,
                'content': message.message[0].content,
                'read_message': read,
                'timestamp': str(message.message[0].timestamp)[:16]
                }
        else:
            data_message = {
                'first_name': message.members.all()[0].profile.first_name + ' ' + message.members.all()[0].profile.last_name,
                'image': message.members.all()[0].profile.image.url,
                'slug': message.members.all()[0].profile.slug,
                'id': message.members.all()[0].profile.id,
                'room_id': message.id,
                'content': message.message[0].content,
                'read_message': read,
                'timestamp': str(message.message[0].timestamp)[:16]
                }
        return data_message

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['user'].id
        self.room_group_name = 'user_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
