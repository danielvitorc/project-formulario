from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import  DiretorForm
from ..models import Chamado

@login_required
def diretor_view(request):
    chamados = Chamado.objects.filter(assinatura_gestor__isnull=False).exclude(assinatura_gestor='').order_by('-id')

    if request.method == 'POST':
        chamado_id = request.POST.get('chamado_id')
        chamado = Chamado.objects.get(id=chamado_id)

        form_diretor = DiretorForm(request.POST, request.FILES, instance=chamado)

        if form_diretor.is_valid():
            form_diretor.save()
            return redirect('diretor_view')
    else:
        form_diretor = DiretorForm()

    return render(request, 'formulario/diretor.html', {'chamados': chamados, 'form_diretor': form_diretor})


@login_required
def registros_diretor(request):
    chamados = Chamado.objects.filter(assinatura_rh_dp__isnull=False).exclude(assinatura_rh_dp='').order_by('-id')

    return render(request, 'formulario/registros_diretor.html', {
        'chamados': chamados
    })