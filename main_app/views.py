from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
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

class KidCreate(CreateView):
    model = Kid
    fields = '__all__'
    # success_url = '/kid/'

class KidUpdate(UpdateView):
    model = Kid
    fields = ['description', 'age']

class KidDelete(DeleteView):
    model = Kid
    success_url = '/index/'