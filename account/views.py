from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.utils.translation import gettext_lazy as _

from chat.models import Room
from chat.views import pleaseLogin

from .forms import RegisterUserForm, SetPasswordForm, PasswordResetForm
from .models import HeadUserAccess
from .tokens import account_activation_token

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'account/login.html', {'alert': True})
        
    else:
        return render(request, 'account/login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def activateEmail(request, user, to_email):
    mail_subject= _("Aktivizē savu lietotāja kontu.")
    message = render_to_string('account/activate.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        return True
    else:
        return False

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user=None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        return render(request, 'message.html', {
            'title': _('Konts tika aktivizēts!'),
            'text': _('Tagad Jūs varat pieslēgties ar jauno kontu.'),
        })
    
    return render(request, 'message.html', {
        'title': _('Aktivizēšanas saite ir nederīga!'),
        'text': _('Izveido jaunu kontu vai sazinies ar palīdzības komandu.'),
    })

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            if activateEmail(request, user, form.cleaned_data.get('email')):
                return render(request, 'message.html', {
                    'title': _('Konts ir gandrīz izveidots!'),
                    'text': _('Lai pabeigtu konta izveidi, Jums jādodas uz aktivizēšanas saiti, kas Jums tikko tika nosūtīta uz e-pastu ' + user.email + '!'),
                })
            else:
                return render(request, 'message.html', {
                    'title': _('Neizdevās aktivizēt kontu!'),
                    'text': _('Tika veikts neveiksmīgs mēģinājums nosūtīt aktivizēšanas saiti uz ' + user.email + ' . Lūdzu pārbaudiet, vai esat pareizi ievadījuši e-pastu!'),
                })
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
            'title': _('Nav pieejas'),
            'text': _('Pārliecinies, vai esi pieslēdzies pareizajam kontam.'),
        })
    
    org_rooms = Room.objects.filter(is_complete=False)
    rooms = []
    for room in org_rooms:
        if room.slug.split('-')[0] != 'dm':
            rooms.append(room)
    
    return render(request, 'account/headpanel.html', {
        'rooms': rooms
    })

def password_change(request):
    if not request.user.is_authenticated:
        return pleaseLogin(request)
    user= request.user
    if request.method=='POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'message.html', {
                'title': _('Parole ir nomainīta!'),
                'text': _('Tagad vari pieslēgties kontam ar jauno paroli.'),
            })
        else:
            return render(request, 'message.html', {
                'title': _('Paroles mainīšana neizdevās!'),
                'text': _('Mēģiniet vēlreiz vai sazinaties ar palīdzības komandu.'),
            })
            
    form = SetPasswordForm(user)
    return render(request, "account/password_change.html", {"form": form})
    
def password_recover(request):
    if request.method=='POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = User.objects.filter(Q(email=user_email)).first()
            if associated_user:
                mail_subject= _("Aktivizē savu lietotāja kontu.")
                message = render_to_string('account/recover_email.html', {
                    'user': associated_user.username,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(mail_subject, message, to=[associated_user.email])
                if email.send():
                    return render(request, 'message.html', {
                        'title': _('Atkopšanas saite nosūtīta!'),
                        'text': _('Uz e-pastu ' + associated_user.email + ' tika nosūtīta saite, lai atkoptu paroli.'),
                    })
                else:
                    return render(request, 'message.html', {
                        'title': _('Radās problēma...'),
                        'text': _('Diemžēl neizdevās nosūtīt atkopšanas saiti uz e-pastu ' + associated_user.email + ' . Mēģiniet vēlreiz vai sazinaties ar palīdzības komandu.'),
                    })
    
    form = PasswordResetForm()
    return render(request, 'account/password_recover.html', {'form': form})

def recovery(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user=None
    
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'message.html', {
                    'title': _('Parole atkopta!'),
                    'text': _('Tagad varat pieslēgties ar jauno paroli'),
                })
        
        form = SetPasswordForm(user, request.POST)
        return render(request, 'account/recovery.html', {'form': form})
    
    return render(request, 'message.html', {
        'title': _('Atkopšanas saite ir nederīga!'),
        'text': _('Mēģini vēlreiz vai sazinies ar palīdzības komandu.'),
    })
