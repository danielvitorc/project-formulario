from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import io
from ..forms import GestorForm, GestorUploadForm
from ..models import Chamado
from docx import Document


@login_required
def gestor_view(request):
    chamados = Chamado.objects.filter(assinatura_sesmt__isnull=False).exclude(assinatura_sesmt='')

    gestor_form = GestorForm()
    upload_form = GestorUploadForm()

    if request.method == 'POST':
        if 'salvar_gestor' in request.POST:
            gestor_form = GestorForm(request.POST, request.FILES)
            if gestor_form.is_valid():
                chamado = gestor_form.save(commit=False)  
                chamado.usuario_gestor = request.user           
                chamado.save()        
                return redirect('gestor_view')

        # Verifica se é o formulário de upload
        elif 'salvar_upload' in request.POST:
            chamado_id = request.POST.get('chamado_id')
            try:
                chamado = Chamado.objects.get(id=chamado_id)
            except Chamado.DoesNotExist:
                chamado = None

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
    })

@login_required
def upload_documento_gestor(request, chamado_id):
    chamado = Chamado.objects.get(id=chamado_id)

    if request.method == 'POST':
        form = GestorUploadForm(request.POST, request.FILES, instance=chamado)
        if form.is_valid():
            chamado.usuario_gestor = request.user
            form.save()
            return redirect('gestor_view')
    else:
        form = GestorUploadForm(instance=chamado)

    return render(request, 'formulario/upload_gestor.html', {
        'form': form,
        'chamado': chamado
    })

@login_required
def registros_gestor(request):
    chamados = Chamado.objects.filter(assinatura_rh_dp__isnull=False, usuario_gestor=request.user).exclude(assinatura_rh_dp='')

    return render(request, 'formulario/registros_gestor.html', {
        'chamados': chamados
    })
