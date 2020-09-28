from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Chat
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Count


User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        chat_id = get_object_or_404(Chat, id=self.room_name)
        messages = Message.objects.order_by('pk').filter(recipient=chat_id)
        count = Chat.objects.filter(id=self.room_name).annotate(Count('members'))
        count = count[0].members__count
        messages.count = count
        #messages.filter().update(is_readed=True)
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


        message = Message.objects.create(
            author=author_user,
            content=data['message'],
            # image_message=data['message'],
            # file_message=data['message'],
            recipient=chat,)

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
        # if message.count >=3:
        #     data_chats={
        #     'author': message.author.username,
        #     'first_name': message.author.profile.first_name + ' ' + message.author.profile.last_name,
        #     'image': message.author.profile.image.url,
        #     'id': message.author.profile.id,
        #     'slug': message.author.profile.slug,
        #     'content': message.content,
        #     # 'image_message': message.image_message,
        #     # 'file_message': message.file_message,
        #     'timestamp': str(message.timestamp)[:16]
        # # }
        # else:
        data_chats={
            'author': message.author.username,
            'first_name': message.author.profile.first_name + ' ' + message.author.profile.last_name,
            'image': message.author.profile.image.url,
            'id': message.author.profile.id,
            'slug': message.author.profile.slug,
            'content': message.content,
            'room_id': message.recipient.id,
            # 'image_message': message.image_message,
            # 'file_message': message.file_message,
            'timestamp': str(message.timestamp)[:16]
        }
        return data_chats

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        body_chat = Chat.objects.order_by('-pk').filter(id=self.room_name)
        body_chat = body_chat[0].members.all()

        for user in body_chat:
            async_to_sync(self.channel_layer.group_add)(
                'user_%s' % user.id,
                self.channel_name
            )


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

        messages = Chat.objects.order_by('-pk').filter(members=self.scope['user'])

        for chat in messages:
            chat_id = get_object_or_404(Chat, id=chat.id)
            message = Message.objects.order_by('-pk').filter(recipient=chat_id)[0:1]
            chat.message = message
            # Получаем количество получателей в комнате
            # Чтобы решить личный чат это или беседа
            count = Chat.objects.filter(id=chat_id.id).annotate(Count('members'))
            count = count[0].members__count
            chat.count = count

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

        # message = Message.objects.create(
        #     author=author_user,
        #     content=data['message'],
        #     recipient=chat)

        # message1 = Message.objects.get(id=message.id)
        chat_id = get_object_or_404(Chat, id=room_name)
        message1 = Message.objects.order_by('-pk').filter(recipient=chat_id)[0:1]

        count = Chat.objects.filter(id=room_name).annotate(Count('members'))
        count = count[0].members__count
        chat.count = count
        chat.message = message1


        content={
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
        # if message.count >= 3:
        #     return {
        #         'first_name': message.group_name,#.author.profile.first_name + ' ' + message.message[0].author.profile.last_name,
        #         # 'image': message.image_chat.url,
        #         'slug': f'/chat/{message.id}',
        #         'room_id': message.id,
        #         'id': message.id,
        #         'content': message.message[0].content,
        #         'timestamp': str(message.message[0].timestamp)[:16]
        #     }
        # else:
        if self.scope['user'] == message.members.all()[0]:
            return {
                'first_name': message.members.all()[1].profile.first_name + ' ' + message.members.all()[1].profile.last_name,
                'image': message.members.all()[1].profile.image.url,
                'slug': f'/account/{message.members.all()[1].profile.slug}',
                'id': message.members.all()[1].profile.id,
                'room_id': message.id,
                'content': message.message[0].content,
                'timestamp': str(message.message[0].timestamp)[:16]
                }

        # return data_chats

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
