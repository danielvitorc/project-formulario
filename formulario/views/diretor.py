from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import  DiretorForm
from ..models import Chamado

@login_required
def diretor_view(request):
    chamados = Chamado.objects.filter(assinatura_gestor__isnull=False).exclude(assinatura_gestor='').order_by('-id')

    if request.method == 'POST':
        form_diretor = DiretorForm(request.POST)
        chamado_id = request.POST.get('chamado_id')

        if form_diretor.is_valid() and chamado_id:
            try:
                chamado = Chamado.objects.get(id=chamado_id)
                chamado.diretor_aprovacao = form_diretor.cleaned_data['diretor_aprovacao']
                chamado.save()
                return redirect('diretor_view')
            except Chamado.DoesNotExist:
                pass  # Pode adicionar uma mensagem de erro se quiser
    else:
        form_diretor = DiretorForm()

    return render(request, 'formulario/diretor.html', {'chamados': chamados, 'form_diretor': form_diretor})