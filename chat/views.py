from chat.models import Room
from django.db import transaction
from django.shortcuts import render, redirect
import haikunator
import random
import string


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, "main/about.html")


def new_room(request):
    '''new_room will randomly create a new room, and redirect to it.
    '''
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)


def chat_room(request, label):
    '''chat_room is the primary room view. It will show a room with
    the latest messages.
    '''

    room, created = Room.objects.get_or_create(label=label)

    # show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])
    context = { 'room': room,
                'messages': messages }

    return render(request, "chat/room.html", context)
