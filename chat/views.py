import json
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Room, Report
from account.models import HeadUserAccess
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _, get_language

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
    
    if room_name.split('-')[0] == 'dm':
        return dm(request, room_name)
        
    if HeadUserAccess.objects.filter(user=request.user.id):
        if not Room.objects.filter(slug=room_name):
            return redirect('/' + get_language() + '/')
        
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
            'title': _('Tev nav pieejas šai istabai'),
            'text': _('Pārbaudi, vai esi pieslēdzies pareizajam kontam.'),
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
    return redirect('/' + get_language() + '/chat/' + str(user_id) + "-" + room_number)

def create(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = User.objects.get(id=body['user_id'])
        count = Room.objects.filter(user=user).count()
        Room.objects.create(name=user.username + " " + str(count), slug=str(user) + "-" + str(count), user=user)
        
        print('donzo')
        return redirect('/' + get_language() + '/chat/join/')
    else:
        return render(request, 'message.html', {
            'title': _('Lapa netika atrasta'),
            'text': '',
        })

def pleaseLogin(request):
    return render(request, 'message.html', {
        'title': _('Tu neesi pieslēdzies'),
        'text': _('Lai turpinātu, tev ir jāpieslēdzās savam kontam'),
    })

def sendChat(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        text = body['message']
        room_name = body['room_name']
        
        if room_name.split('-')[0] == 'dm':
            if str(request.user.id) == room_name.split('-')[1] or str(request.user.id) == room_name.split('-')[2]:
                room_obj = Room.objects.get(slug=room_name)
                room_obj.set_text(room_obj.get_text() + '\n' + str(request.user.username) + ': ' + str(text))
                room_obj.save()
        
        if HeadUserAccess.objects.filter(user=request.user.id) or str(request.user.id) == room_name:
            room_obj = Room.objects.get(slug=room_name)
            room_obj.set_text(room_obj.get_text() + '\n' + str(request.user.username) + ': ' + str(text))
            room_obj.save()
        
        return redirect('/' + get_language() + '/chat/' + room_name)
    
    return redirect('/' + get_language() + '/')

def complete(request, room_number):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    
    if not HeadUserAccess.objects.filter(user=request.user.id):
        return redirect('/' + get_language() + '/')
    
    room = Room.objects.get(slug=room_number)
    room.complete()
    
    Report.objects.create(client=str(room.user.username), head=str(request.user.username), chat=str(room.get_text()), room_name=room_number)
    
    return redirect('/' + get_language() + reverse('account:headpanel'))

def delete(request, room_number):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    
    room_slug = room_number.split('-')
    
    if str(request.user.id) != room_slug[0]:
        return redirect('/' + get_language() + "/")
    
    room = Room.objects.get(slug=room_number)
    room.delete()
    
    return redirect('/' + get_language() + reverse('account:dashboard'))

def dm(request, dm_name):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    
    info = dm_name.split('-')
    
    if str(request.user.id) == info[1] or str(request.user.id) == info[2]:
        if not Room.objects.filter(slug=dm_name):
            return redirect('/' + get_language() + '/')
        
        dm_room = Room.objects.get(slug=dm_name)
        user = User.objects.get(id=int(info[2]))
        head = HeadUserAccess.objects.get(user=user)
        
        return render(request, 'chat/chatroom.html', {
            'room_name': dm_room.slug,
            'text': dm_room.get_text(),
            'is_complete': dm_room.is_complete,
        })
    
    return redirect('/' + get_language() + '/')

def createdm(request, slug):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    
    if not HeadUserAccess.objects.filter(slug=slug):
        return redirect('/' + get_language() + '/')
    
    head = HeadUserAccess.objects.get(slug=slug)
    
    if Room.objects.filter(slug=slugify("dm-" + str(request.user.id) + "-" + str(head.user.id))):
        return render(request, 'message.html', {
            'title': _('Tāda istaba jau eksistē'),
            'text': _('Saraksti var atrast savā profilā'),
        })
    
    Room.objects.create(
        name="Sarakste ar " + head.name,
        slug=slugify("dm-" + str(request.user.id) + "-" + str(head.user.id)),
        user=request.user,
        text="Uzsākta sarakste.\n"
    )
    
    return redirect('/' + get_language() + reverse('account:dashboard'))
