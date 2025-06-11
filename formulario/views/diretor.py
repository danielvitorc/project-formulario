from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from ..forms import  DiretorForm
from ..models import Chamado
from django.contrib import messages

@login_required
def diretor_view(request):
    chamados = Chamado.objects.filter(
        assinatura_gestor__isnull=False
    ).exclude(assinatura_gestor='').order_by('-id')

    form_diretor = DiretorForm()  

    if request.method == 'POST':
        chamado_id = request.POST.get('chamado_id')
        diretor_aprovacao = request.POST.get('diretor_aprovacao')
        assinatura_diretor = request.FILES.get('assinatura_diretor')

        chamado = Chamado.objects.get(id=chamado_id)

        if diretor_aprovacao is not None and assinatura_diretor is not None:
            chamado.diretor_aprovacao = True if diretor_aprovacao == 'True' else False
            chamado.assinatura_diretor = assinatura_diretor
            try:
                chamado.full_clean()  # VALIDAÇÃO ACONTECE AQUI
                chamado.save()
                messages.success(request, 'Aprovação realizada com sucesso!')
                return redirect('diretor_view')
            except ValidationError as e:
                erros = e.message_dict.get('__all__')
                if erros:
                    messages.error(request, f'Erro na validação: {erros[0]}')
                else:
                    messages.error(request, f'Erro na validação: {e.message_dict}')
        else:
            messages.error(request, 'Preencha todos os campos corretamente.')

    return render(
        request,
        'formulario/diretor.html',
        {'chamados': chamados, 'form_diretor': form_diretor}
    )



@login_required
def registros_diretor(request):
    chamados = Chamado.objects.filter(assinatura_rh_dp__isnull=False).exclude(assinatura_rh_dp='').order_by('-id')

    return render(request, 'formulario/registros_diretor.html', {
        'chamados': chamados
    })