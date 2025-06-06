from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import io
from ..forms import GestorForm, GestorUploadForm
from ..models import Chamado
from docx import Document
from django.contrib import messages


@login_required
def gestor_view(request):
    chamados = Chamado.objects.filter(
        assinatura_sesmt__isnull=False, 
        usuario_gestor=request.user
    ).exclude(assinatura_sesmt='').order_by('-id')

    chamados_pendentes = Chamado.objects.filter(
        usuario_gestor=request.user
    ).filter(
        Q(assinatura_rh_dp__isnull=True) | Q(assinatura_rh_dp__exact='')
    ).order_by('-id')

    gestor_form = GestorForm()
    upload_form = GestorUploadForm()

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
        if 'salvar_gestor' in request.POST:
            gestor_form = GestorForm(request.POST, request.FILES)
            if gestor_form.is_valid():
                chamado = gestor_form.save(commit=False)
                chamado.usuario_gestor = request.user
                chamado.save()
                return redirect('gestor_view')

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
                    return redirect('gestor_view')

    return render(request, 'formulario/gestor.html', {
        'gestor_form': gestor_form,
        'upload_form': upload_form,
        'chamados': chamados,
        'chamados_pendentes': chamados_pendentes,
        'chamados_nao_aptos': chamados_nao_aptos  # <- passa pro template
    })


@login_required
def registros_gestor(request):
    chamados = Chamado.objects.filter(assinatura_rh_dp__isnull=False, usuario_gestor=request.user).exclude(assinatura_rh_dp='')

    return render(request, 'formulario/registros_gestor.html', {
        'chamados': chamados
    })
