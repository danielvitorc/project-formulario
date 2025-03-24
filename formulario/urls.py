from django.urls import path
from .views import cadastrar_chamado

urlpatterns = [
    path('', cadastrar_chamado, name='cadastrar_chamado'),
]