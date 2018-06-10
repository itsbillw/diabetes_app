from django.urls import path

from . import views

app_name = 'data'
urlpatterns = [
    path('', views.index, name='index'),
    path('view/', views.view, name='view'),
    path('upload/', views.upload, name='upload'),
]
