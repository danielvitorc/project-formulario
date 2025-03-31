from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view, name='login'),
    path('cadastrar_chamado', views.cadastrar_chamado, name='cadastrar_chamado'),
]