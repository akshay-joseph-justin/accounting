from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    path('ledger/', views.ledger, name='ledger'),
    path('add-ledger/', views.add_ledger, name='add-ledger'),

    path('wallet/', views.wallet, name='wallet'),

    path('', views.service, name='service'),
    path('', views.contact, name='contact'),
]
