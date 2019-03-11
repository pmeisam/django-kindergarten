from django.shortcuts import render
from django.http import HttpResponse
from .models import Kid
# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def kids_index(request):
    kids = Kid.objects.all()
    return render(request, "kids/index.html", {'kids': kids})

def kid_detail(request, kid_id):
    kid = Kid.objects.get(id=kid_id)
    return render( request, 'kids/detail.html', {'kid': kid} )