from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import RHDPForm
from ..models import Chamado


@login_required
def rh_dp_view(request):
    chamados = Chamado.objects.filter(upload_gestor__isnull=False).exclude(upload_gestor='')

    return render(request, 'formulario/rh_dp.html', {'chamados': chamados})

@login_required
def rh_dp_editar(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)

    if request.method == 'POST':
        form_rh_dp = RHDPForm(request.POST, request.FILES, instance=chamado)
        if form_rh_dp.is_valid():
            form_rh_dp.save()
            messages.success(request, 'Formulário RH/DP salvo com sucesso!')
            return redirect('rh_dp_view')
    else:
        form_rh_dp = RHDPForm(instance=chamado)

    return render(request, 'formulario/include/rh_dp_editar.html', {'form_rh_dp': form_rh_dp, 'chamado': chamado})

@login_required
def registros_rh_dp(request):
    chamados = Chamado.objects.filter(assinatura_rh_dp__isnull=False).exclude(assinatura_rh_dp='')

    return render(request, 'formulario/registros_rh_dp.html', {
        'chamados': chamados
    })