from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Kid
from .forms import FeedingForm
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
    feeding_form = FeedingForm()
    return render( request, 'kids/detail.html', {'kid': kid, 'feeding_form': feeding_form} )

def add_feeding(request, kid_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.kid_id = kid_id
        new_feeding.save()
    return redirect('detail', kid_id=kid_id)

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

