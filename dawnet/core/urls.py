from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('', views.service, name='service'),
    path('', views.contact, name='contact'),
]
