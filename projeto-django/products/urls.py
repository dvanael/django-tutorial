from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('sobre/', about, name='about'),
    path('Categoria/', product_list, name='product-list'),
    path('produtos/cadastrar/', product_create, name='product-create'),
    path('produtos/<int:pk>/', product_detail, name='product-detail'),
    path('produtos/<int:pk>/atualizar/', product_update, name='product-update'),
    path('produtos/<int:pk>/deletar/', product_delete, name='product-delete'),
]