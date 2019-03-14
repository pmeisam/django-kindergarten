from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('index/', views.kids_index, name="index"),
    path('kid/<int:kid_id>/', views.kid_detail, name='detail'),
    path('kid/create/', views.KidCreate.as_view(), name='kids_create'),
    path('kid/<int:pk>/update/', views.KidUpdate.as_view(), name='kids_update'),
    path('kid/<int:pk>/delete/', views.KidDelete.as_view(), name='kids_delete'),
    path('kid/<int:kid_id>/add_feeding/', views.add_feeding, name="add_feeding"),
    path('toys/', views.toys_index, name='toys'),
    path('toys/create/', views.ToyCreate.as_view(), name="toys_create"),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name="toys_detail"),
    path('toys/<int:pk>/edit/', views.ToyUpdate.as_view(), name="toys_update"),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name="toys_delete"),
    path('toys/<int:kid_id>/assoc_toy/<int:toy_id>', views.assoc_toy, name="assoc_toy"),
    path('kids/<int:kid_id>/add_photo/', views.add_photo, name="add_photo"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
]   