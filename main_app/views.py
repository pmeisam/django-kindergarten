from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
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

def kids_index(request):
    kids = Kid.objects.all()
    return render(request, "kids/index.html", {'kids': kids})

def kid_detail(request, kid_id):
    kid = Kid.objects.get(id=kid_id)
    toys_kid_doesnt_have = Toy.objects.exclude(id__in = kid.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render( request, 'kids/detail.html', {
        'kid': kid, 
        'feeding_form': feeding_form, 
        'toys': toys_kid_doesnt_have
        } )

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

def toys_index(request):
    toys = Toy.objects.all()
    return render(request, 'toys/index.html', {'toys': toys})

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyDetail(DetailView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

def assoc_toy( request, kid_id, toy_id ):
    Kid.objects.get(id=kid_id).toys.add(toy_id)
    return redirect('detail', kid_id=kid_id)

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