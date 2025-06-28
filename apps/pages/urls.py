from django.urls import path
from .views import index, register_view

urlpatterns = [
    path('', index, name='index'),           # rota principal
    path('register/', register_view, name='register'),  # rota para registro
]
