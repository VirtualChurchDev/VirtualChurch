from django.shortcuts import redirect, render, reverse
from .models import News, Church
from account.models import HeadUserAccess

def home(request):
    return render(request, 'church/home.html')

def pricing(request):
    return render(request, 'church/pricing.html')

def newsall(request):
    return render(request, 'church/news.html', {
        'news': News.objects.all()
    })

def info(request):
    return render(request, 'church/info.html')

def churchbrowser(request):
    churches = Church.objects.all()
    return render(request, 'church/churchbrowser.html',{
        'churches': churches,
    })

def singlechurch(request, slug):
    if not Church.objects.filter(slug=slug):
        return redirect(reverse('church:churchbrowser'))
    
    single = Church.objects.get(slug=slug)
    return render(request, 'church/churchsingle.html',{
        'single': single,
    })

def singlechurchtour(request, slug):
    if not Church.objects.filter(slug=slug):
        return redirect(reverse('church:churchbrowser'))
    
    single = Church.objects.get(slug=slug)
    return render(request, 'church/churchsingletour.html',{
        'single': single,
    })

def headbrowser(request):
    heads=HeadUserAccess.objects.all()
    return render(request, 'church/headbrowser.html', {
        'heads': heads,
    })

def singlehead(request, slug):
    if not HeadUserAccess.objects.filter(slug=slug):
        return redirect(reverse('church:headbrowser'))
    
    single = HeadUserAccess.objects.get(slug=slug)
    return render(request, 'church/headsingle.html', {
        'single': single,
    })
