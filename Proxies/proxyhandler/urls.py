from django.urls import path

from . import views

urlpatterns = [
    path('scrap', views.scrap, name='scrap'),
    path('verify', views.verify, name='verify'),
    path('show', views.show, name='working_proxies'),
    path('test', views.test, name='test')
]
