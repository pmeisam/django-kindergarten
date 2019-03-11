from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('index/', views.kids_index, name="index"),
    path('kid/<int:kid_id>', views.kid_detail, name='detail')
]   