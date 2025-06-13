from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from ..forms import RHDPForm
from ..models import Chamado


@login_required
def rh_dp_view(request):
    chamados = Chamado.objects.filter(assinatura_sesmt__isnull=False, rh_dp_ciente = False, 
    aso = 'Apto', epi_epc = 'Apto', curso_nr10 = 'Apto', curso_sep = 'Apto', curso_nr35 = 'Apto'
    ).exclude(assinatura_sesmt='').order_by('-id')

    chamados_pendentes = Chamado.objects.filter(
    Q(aso='Não apto') |
    Q(epi_epc='Não apto') |
    Q(curso_nr10='Não apto') |
    Q(curso_sep='Não apto') |
    Q(curso_nr35='Não apto')
).order_by('-id')

    return render(request, 'formulario/rh_dp.html', {'chamados': chamados , 'chamados_pendentes' : chamados_pendentes })

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
    chamados = Chamado.objects.filter(assinatura_rh_dp__isnull=False).exclude(assinatura_rh_dp='').order_by('-id')

    return render(request, 'formulario/registros_rh_dp.html', {
        'chamados': chamados
    })

def rh_dp_ciente(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    chamado.rh_dp_ciente = True
    chamado.save()
    return redirect('rh_dp_view') 