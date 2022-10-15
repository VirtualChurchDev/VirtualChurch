from contextlib import redirect_stderr
import json
from django.shortcuts import render, redirect, reverse
from .models import Room, Report
from account.models import HeadUserAccess
from django.contrib.auth.models import User

def index(request):
    rooms = None
    if request.user.is_authenticated:
        if Room.objects.filter(user=request.user):
            rooms = Room.objects.filter(user=request.user)
    
    return render(request, 'chat/index.html', {
        'rooms': rooms
    })

def room(request, room_name):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
        
    if HeadUserAccess.objects.filter(user=request.user.id):
        if not Room.objects.filter(slug=room_name):
            return redirect('/')
        
        room = Room.objects.get(slug=room_name)
        text = room.get_text()
        
        return render(request, 'chat/chatroom.html', {
            'room_name': room_name,
            'text': text,
            'is_head': True,
        })
    
    room_slug = room_name.split('-')
    
    if str(request.user.id) != room_slug[0]:
        return render(request, 'message.html', {
            'title': 'Tev nav pieejas šai istabai',
            'text': 'Pārbaudi, vai esi pieslēdzies pareizajam kontam.',
        })
        
    room = Room.objects.get(slug=room_name)
    text = room.get_text()
    
    return render(request, 'chat/chatroom.html', {
        'room_name': room_name,
        'text': text,
        'is_complete': room.is_complete,
    })
    
def payment(request):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    
    return render(request, 'chat/payment.html')

def join(request, room_number):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    user_id = request.user.id
    return redirect('/chat/' + str(user_id) + "-" + room_number)

def create(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = User.objects.get(id=body['user_id'])
        count = Room.objects.filter(user=user).count()
        Room.objects.create(name=user.username + " " + str(count), slug=str(user.id) + "-" + str(count), user=user)
        
        print('donzo')
        return redirect('/chat/join/')
    else:
        return render(request, 'message.html', {
            'title': 'Lapa netika atrasta',
            'text': '',
        })

def pleaseLogin(request):
    return render(request, 'message.html', {
        'title': 'Tu neesi pieslēdzies',
        'text': 'Lai turpinātu, tev ir jāpieslēdzās savam kontam',
    })

def sendChat(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        text = body['message']
        room_name = body['room_name']
        if HeadUserAccess.objects.filter(user=request.user.id) or str(request.user.id) == room_name:
            room_obj = Room.objects.get(slug=room_name)
            room_obj.set_text(room_obj.get_text() + '\n' + str(request.user.username) + ': ' + str(text))
            room_obj.save()
    
    return redirect(reverse('chat:join'))

def complete(request, room_number):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    
    if not HeadUserAccess.objects.filter(user=request.user.id):
        return redirect('/')
    
    room = Room.objects.get(slug=room_number)
    room.complete()
    
    Report.objects.create(client=str(room.user.username), head=str(request.user.username), chat=str(room.get_text()), room_name=room_number)
    
    return redirect(reverse('account:headpanel'))

def delete(request, room_number):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    
    room_slug = room_number.split('-')
    
    if str(request.user.id) != room_slug[0]:
        return redirect("/")
    
    room = Room.objects.get(slug=room_number)
    room.delete()
    
    return redirect(reverse('account:dashboard'))
