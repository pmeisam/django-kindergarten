from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Kid, Toy, Photo
from .forms import FeedingForm

import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollectormeisam'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def kids_index(request):
    kids = Kid.objects.filter(user = request.user)
    return render(request, "kids/index.html", {'kids': kids})

@login_required
def kid_detail(request, kid_id):
    kid = Kid.objects.get(id=kid_id)
    toys_kid_doesnt_have = Toy.objects.exclude(id__in = kid.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render( request, 'kids/detail.html', {
        'kid': kid, 
        'feeding_form': feeding_form, 
        'toys': toys_kid_doesnt_have
        } )

@login_required
def add_feeding(request, kid_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.kid_id = kid_id
        new_feeding.save()
    return redirect('detail', kid_id=kid_id)

class KidCreate(LoginRequiredMixin, CreateView):
    model = Kid
    fields = '__all__'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class KidUpdate(LoginRequiredMixin, UpdateView):
    model = Kid
    fields = ['description', 'age']

class KidDelete(LoginRequiredMixin, DeleteView):
    model = Kid
    success_url = '/index/'

@login_required
def toys_index(request):
    toys = Toy.objects.all()
    return render(request, 'toys/index.html', {'toys': toys})

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

@login_required
def assoc_toy( request, kid_id, toy_id ):
    Kid.objects.get(id=kid_id).toys.add(toy_id)
    return redirect('detail', kid_id=kid_id)

@login_required
def add_photo(request, kid_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object
            photo = Photo(url=url, kid_id=kid_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', kid_id=kid_id)

@login_required
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credentials - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
