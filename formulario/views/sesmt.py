from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import SESMTForm
from ..models import Chamado

@login_required
def sesmt_view(request):
    chamados = Chamado.objects.filter(diretor_aprovacao=True, sesmt_ciente = False).order_by('-id')

    return render(request, 'formulario/sesmt.html', {'chamados': chamados})

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
    chamados = Chamado.objects.filter(assinatura_rh_dp__isnull=False).exclude(assinatura_rh_dp='').order_by('-id')

    return render(request, 'formulario/registros_sesmt.html', {
        'chamados': chamados
    })

def sesmt_ciente(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    chamado.sesmt_ciente = True
    chamado.save()
    return redirect('sesmt_view')  # Ou onde quiser redirecionar