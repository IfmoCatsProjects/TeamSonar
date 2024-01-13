from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Message, ChatRoom
from django.conf import settings

User = settings.AUTH_USER_MODEL


def message(request):
    sender = request.POST.get('sender')
    receiver = request.POST.get('receiver')
    msg = request.POST.get('message')
    if Message.objects.create(sender=User.objects.get(id=sender), receiver=User.objects.get(id=receiver), text=msg):
        return HttpResponse('OK')
    return HttpResponse('ERR')


def message_delete(request):
    message_id = request.POST.get('message_id')
    if Message.objects.get(id=message_id).delete():
        return HttpResponse('OK')
    return HttpResponse('ERR')


class ChatRoomView(View):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        chat = ChatRoom.objects.get(id=request.POST.get('chat_id'))
        messages = Message.objects.filter(room=chat)

        result = []
        for msg in messages:
            result.append({
                'sender': msg.sender.username,
                'receiver': msg.receiver.username,
                'text': msg.text
            })


class ChatsView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        chats = ChatRoom.objects.filter(users__in=user)

        result = []

        for chat in chats:
            result.append(
                {
                    'id': chat.roomId,
                    'members': chat.users
                }
            )

        return JsonResponse(result, safe=False)
