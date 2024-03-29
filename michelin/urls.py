from django.urls import path

from . import views

app_name = 'michelin'

urlpatterns = [
    path('', views.search, name='base'),
    path('404', views.error404, name='error404'),
    path('query/', views.query, name='query'),
    path('details/<id>', views.fetch_details, name='fetch_details'),
]