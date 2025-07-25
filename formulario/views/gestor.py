from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from ..forms import GestorForm
from ..models import Chamado
from docx import Document
from django.contrib import messages


@login_required
def gestor_view(request):

    chamados = Chamado.objects.filter(
        assinatura_sesmt__isnull=False, 
        usuario_gestor=request.user,
        gestor_ciente=False
    ).exclude(assinatura_sesmt__isnull=True).order_by('-id')

    chamados_pendentes = Chamado.objects.filter(
        usuario_gestor=request.user,
        gestor_ciente=False
    ).order_by('-id')

    gestor_form = GestorForm()

    # Mapeia quais chamados não estão aptos
    chamados_nao_aptos = []
    for chamado in chamados:
        if any([
            chamado.aso == 'Não apto',
            chamado.epi_epc == 'Não apto',
            chamado.curso_nr10 == 'Não apto',
            chamado.curso_sep == 'Não apto',
            chamado.curso_nr35 == 'Não apto',
        ]):
            chamados_nao_aptos.append(chamado.id)

    if request.method == 'POST':
        gestor_form = GestorForm(request.POST, request.FILES)
        if gestor_form.is_valid():
            chamado = gestor_form.save(commit=False, user=request.user)
            chamado.usuario_gestor = request.user
            chamado.save()
            return redirect('gestor_view')

        '''
        elif 'salvar_upload' in request.POST:
            chamado_id = request.POST.get('chamado_id')
            chamado = Chamado.objects.filter(id=chamado_id).first()

            # Bloqueia o upload se for "não apto"
            if chamado and chamado.id in chamados_nao_aptos:
                messages.error(request, "Não é possível fazer o upload. Um ou mais campos estão marcados como 'Não apto'.")
                return redirect('gestor_view')

            if chamado:
                upload_form = GestorUploadForm(request.POST, request.FILES)
                if upload_form.is_valid():
                    chamado.upload_gestor = upload_form.cleaned_data['upload_gestor']
                    chamado.save()
        '''

    return render(request, 'formulario/gestor.html', {
        'gestor_form': gestor_form,
        'chamados': chamados,
        'chamados_pendentes': chamados_pendentes,
        'chamados_nao_aptos': chamados_nao_aptos 
    })


@login_required
def registros_gestor(request):
    chamados = Chamado.objects.filter(assinatura_rh_dp__isnull=False, usuario_gestor=request.user).exclude(assinatura_rh_dp__isnull=True)

    return render(request, 'formulario/registros_gestor.html', {
        'chamados': chamados
    })

def gestor_ciente(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    chamado.gestor_ciente = True
    chamado.save()
    return redirect('gestor_view')  # Ou onde quiser redirecionar

@require_POST
def excluir_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    motivo = request.POST.get('motivo')

    if not motivo:
        messages.error(request, "É obrigatório informar o motivo da exclusão.")
        return redirect('gestor_view')

    try:
        chamado.delete(user=request.user, motivo_exclusao=motivo)
        messages.success(request, "Chamado excluído com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao excluir: {e}")

    return redirect('gestor_view')
