from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from ..forms import  DiretorForm
from ..models import Chamado
from django.contrib import messages

@login_required
def diretor_view(request):
    chamados = Chamado.objects.filter(
        assinatura_gestor__isnull=False
    ).exclude(assinatura_gestor__isnull=True).order_by('-id')

    form_diretor = DiretorForm()  

    if request.method == 'POST':
        chamado_id = request.POST.get('chamado_id')
        chamado = get_object_or_404(Chamado, id=chamado_id)

        form_diretor = DiretorForm(request.POST, request.FILES, instance=chamado)

        if form_diretor.is_valid():
            try:
                assinar = form_diretor.cleaned_data.get('assinar_como_diretor', False)
                form_diretor.save(user=request.user if assinar else None)
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