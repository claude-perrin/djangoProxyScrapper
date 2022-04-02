from django.urls import path

from . import views

urlpatterns = [
    path('scrap', views.scrap, name='scrap'),
    path('verify', views.verify, name='scrap')
]
