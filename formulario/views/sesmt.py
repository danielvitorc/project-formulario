from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import SESMTForm
from ..models import Chamado, ChamadoBackup

@login_required
def sesmt_view(request):
    pendentes = Chamado.objects.filter(
        assinatura_gestor__isnull=False,
        assinatura_sesmt__isnull=True
    ).order_by('-id')

    sesmt_preenchidos = Chamado.objects.filter(
        assinatura_sesmt__isnull=False,
        assinatura_rh_dp__isnull=True
    ).order_by('-id')

    # 3️⃣ Chamados com RH/DP preenchido
    rh_preenchidos = Chamado.objects.filter(
        assinatura_rh_dp__isnull=False
    ).order_by('-id')

    return render(request, 'formulario/sesmt.html', {
        'pendentes': pendentes,
        'sesmt_preenchidos': sesmt_preenchidos,
        'rh_preenchidos': rh_preenchidos,})

@login_required
def sesmt_editar(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)

    if request.method == 'POST':
        form = SESMTForm(request.POST, request.FILES, instance=chamado)
        if form.is_valid():
            assinar = form.cleaned_data.get('assinar_como_sesmt', False)
            form.save(user=request.user if assinar else None)
            messages.success(request, 'Formulário SESMT salvo com sucesso!')
            return redirect('sesmt_view')
    else:
        form = SESMTForm(instance=chamado)

    return render(request, 'formulario/include/sesmt_editar.html', {'form': form, 'chamado': chamado})

@login_required
def registros_sesmt(request):
    chamados = Chamado.objects.filter(assinatura_rh_dp__isnull=False).exclude(assinatura_rh_dp__isnull=True).order_by('-id')

    return render(request, 'formulario/registros_sesmt.html', {
        'chamados': chamados
    })

def sesmt_ciente(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    chamado.sesmt_ciente = True
    chamado.save()
    return redirect('sesmt_view')  # Ou onde quiser redirecionar

def lista_chamados_backup(request):

    matricula_query = request.GET.get("matricula") or ""  
    chamados_backup = ChamadoBackup.objects.all().order_by('-data_exclusao')

    if matricula_query:
        chamados_backup = chamados_backup.filter(matricula__icontains=matricula_query)

    return render(request, 'formulario/lista_backup.html', {
        'chamados_backup': chamados_backup,
        'matricula_query': matricula_query  # envia de volta para manter no input
    })