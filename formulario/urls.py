from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view, name='login'),
    path('gestor/', views.gestor_view, name='gestor_view'),
    path('diretor/', views.diretor_view, name='diretor_view'),
    path('sesmt/', views.sesmt_view, name='sesmt_view'),
    path('sesmt/editar/<int:pk>/', views.sesmt_editar, name='sesmt_editar'),
    path('rh_dp/', views.rh_dp_view, name='rh_dp_view'),
    path('rh_dp/editar/<int:pk>/', views.rh_dp_editar, name='rh_dp_editar'),
]