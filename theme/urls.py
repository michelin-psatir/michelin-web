from django.urls import path

from . import views

app_name = 'theme'

urlpatterns = [
    path('', views.base, name='base'),
    path('test-dev/1', views.test_dev1, name='test_dev1'),
    path('test-dev/2', views.test_dev2, name='test_dev2'),
    path('test-dev/3', views.test_dev3, name='test_dev3'),
]