from django.urls import path
from .views import auth, gestor, diretor, sesmt, rh_dp, excel

urlpatterns = [
    path('',auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('gestor/', gestor.gestor_view, name='gestor_view'),
    path('registros-gestor/', gestor.registros_gestor, name='registros_gestor'),
    path('diretor/', diretor.diretor_view, name='diretor_view'),
    path('sesmt/', sesmt.sesmt_view, name='sesmt_view'),
    path('registros-sesmt/', sesmt.registros_sesmt, name='registros_sesmt'),
    path('sesmt/editar/<int:pk>/', sesmt.sesmt_editar, name='sesmt_editar'),
    path('rh_dp/', rh_dp.rh_dp_view, name='rh_dp_view'),
    path('registros-rh_dp/', rh_dp.registros_rh_dp, name='registros_rh_dp'),
    path('rh_dp/editar/<int:pk>/', rh_dp.rh_dp_editar, name='rh_dp_editar'),
    path('download_per/<int:registro_id>/', excel.download_per_excel, name='download_per_excel'),
]