from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterUserForm
from .models import HeadUserAccess
from chat.models import Room
from chat.views import pleaseLogin

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'account/login.html', {'alert': 'Invalid username or password!'})
        
    else:
        return render(request, 'account/login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterUserForm()

    return render(request, 'account/register.html', {
        'form': form,
    })

def dashboard(request):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    
    user = User.objects.get(id=request.user.id)
    rooms = Room.objects.filter(user=user)
    
    is_headuser = False
    
    if HeadUserAccess.objects.filter(user=request.user.id):
        is_headuser = True
    
    return render(request, 'account/dashboard.html', {
        'is_headuser': is_headuser,
        'rooms': rooms
    })

def headpanel(request):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    
    if not HeadUserAccess.objects.filter(user=request.user.id):
        return render(request, 'message.html', {
            'title': 'Nav pieejas',
            'text': 'Pārliecinies, vai esi pieslēdzies pareizajam kontam.',
        })
    
    org_rooms = Room.objects.filter(is_complete=False)
    rooms = []
    for room in org_rooms:
        if room.slug.split('-')[0] != 'dm':
            rooms.append(room)
    
    return render(request, 'account/headpanel.html', {
        'rooms': rooms
    })
