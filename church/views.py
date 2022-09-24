from django.shortcuts import render
from .models import News

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
