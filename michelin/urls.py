from django.urls import path

from . import views

app_name = 'michelin'

urlpatterns = [
    path('', views.search, name='base'),
    path('query/', views.query, name='query'),
]