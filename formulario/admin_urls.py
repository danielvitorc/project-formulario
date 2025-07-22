from django.urls import path
from .views import admin_views

urlpatterns = [
    path("dashboard/", admin_views.admin_dashboard, name="admin_dashboard"),
    path("usuarios/", admin_views.admin_usuarios, name="admin_usuarios"),
    path("usuarios/criar/", admin_views.admin_criar_usuario, name="admin_criar_usuario"),
    path("usuarios/<int:user_id>/editar/", admin_views.admin_editar_usuario, name="admin_editar_usuario"),
    path("usuarios/<int:user_id>/trocar-senha/", admin_views.admin_trocar_senha, name="admin_trocar_senha"),
    path("usuarios/<int:user_id>/bloquear/", admin_views.admin_bloquear_usuario, name="admin_bloquear_usuario"),
    path("usuarios/<int:user_id>/excluir/", admin_views.admin_excluir_usuario, name="admin_excluir_usuario"),
]

