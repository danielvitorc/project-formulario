from django.urls import path, include
from .views import auth, gestor, diretor, sesmt, rh_dp, excel, analitico

urlpatterns = [
    path('',auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('gestor/', gestor.gestor_view, name='gestor_view'),
    path('registros-gestor/', gestor.registros_gestor, name='registros_gestor'),
    path('diretor/', diretor.diretor_view, name='diretor_view'),
    path('registros-diretor/', diretor.registros_diretor, name='registros_diretor'),
    path('sesmt/', sesmt.sesmt_view, name='sesmt_view'),
    path('registros-sesmt/', sesmt.registros_sesmt, name='registros_sesmt'),
    path('sesmt/editar/<int:pk>/', sesmt.sesmt_editar, name='sesmt_editar'),
    path('chamados/backup/', sesmt.lista_chamados_backup, name='lista_chamados_backup'),
    path('rh_dp/', rh_dp.rh_dp_view, name='rh_dp_view'),
    path('registros-rh_dp/', rh_dp.registros_rh_dp, name='registros_rh_dp'),
    path('rh_dp/editar/<int:pk>/', rh_dp.rh_dp_editar, name='rh_dp_editar'),
    path('download_per/<int:registro_id>/', excel.download_per_excel, name='download_per_excel'),
    path('exportar-chamados/', excel.exportar_chamados_excel, name='exportar_chamados'),
    path('chamado/<int:pk>/gestor_ciente/', gestor.gestor_ciente, name='gestor_ciente'),
    path('chamado/<int:pk>/sesmt_ciente/', sesmt.sesmt_ciente, name='sesmt_ciente'),
    path('chamado/<int:pk>/rh_dp_ciente/', rh_dp.rh_dp_ciente, name='rh_dp_ciente'),
    path('chamado/excluir/<int:id>/', gestor.excluir_chamado, name='excluir_chamado'),
    path('analitico/', analitico.analitico_view, name='analitico_view'),
    path('analitico/dados/', analitico.analitico_dados_view, name='analitico_dados_view'),
    
    # URLs Administrativas
    path('admin-panel/', include('formulario.admin_urls')),
]