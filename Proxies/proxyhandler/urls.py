from django.urls import path

from . import views


# show main page
urlpatterns = [
    path('', views.main_page, name='scrap'),
    path('scrap', views.scrap, name='scrap'),
    path('verify', views.verify, name='verify'),
    path('show', views.show, name='working_proxies'),
    path('download/txt/', views.download_txt, name='download'),
    path('download/csv/', views.download_csv, name='download'),
    path('test', views.test, name='test')
    # path('celery', views.celery)
]
