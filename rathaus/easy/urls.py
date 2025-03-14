from django.urls import path
from . import views

urlpatterns = [
    # path('', views.backend, name='backend'),
    path('', views.index, name='index'),
    path('success/', views.backend, name='backend'),
]