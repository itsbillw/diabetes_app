from django.urls import path

from . import views

app_name = 'data'
urlpatterns = [
    path('', views.index, name='index'),
    path('view/', views.view, name='view'),
    path('upload/', views.upload, name='upload'),
    path('cgms/', views.cgms_data, name='cgms_data'),
    path('save/', views.cgms_save, name='cgms_save'),
]
