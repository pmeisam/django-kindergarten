from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('index/', views.kids_index, name="index"),
    path('kid/<int:kid_id>', views.kid_detail, name='detail'),
    path('kid/create/', views.KidCreate.as_view(), name='kids_create'),
    path('kid/<int:pk>/update/', views.KidUpdate.as_view(), name='kids_update'),
    path('kid/<int:pk>/delete/', views.KidDelete.as_view(), name='kids_delete'),
]   