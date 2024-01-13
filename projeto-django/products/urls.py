from django.urls import path
from .views import index

urlpatterns = [
    path('inicio/', index, name='index'),
]