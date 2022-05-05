from django.urls import path

from . import views

# show main page
urlpatterns = [
    path('', views.main_page, name='scrap'),
    path('scrap', views.scrap, name='scrap'),
    path('verify', views.verify, name='verify'),
    path('show', views.show, name='working_proxies'),
    path('download/<str:method>/', views.Downloader.as_view(), name='download'),
    path('test', views.test, name='test')
]
