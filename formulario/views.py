from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import io
from .forms import GestorForm, DiretorForm, SESMTForm, RHDPForm
from .models import Chamado
from docx import Document

# View de Login



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'gestor':
                return redirect('gestor_view')
            elif user.role == 'diretor':
                return redirect('diretor_view')
            elif user.role == 'rh_dp':
                return redirect('rh_dp_view')
            elif user.role == 'sesmt':
                return redirect('sesmt_view')
            else:
                messages.error(request, 'Usuário sem função definida.')
                return redirect('login')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')

    return render(request, 'formulario/login.html')

@login_required
def gestor_view(request):
    if request.method == 'POST':
        form = GestorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestor_view')  
    else:
        form = GestorForm()

    return render(request, 'formulario/gestor.html', {'form': form})

@login_required
def diretor_view(request):
    chamados = Chamado.objects.filter(assinatura_gestor__isnull=False).exclude(assinatura_gestor='')

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

@login_required
def sesmt_view(request):
    chamados = Chamado.objects.filter(diretor_aprovacao=True)
    
    return render(request, 'formulario/sesmt.html', {'chamados': chamados})

@login_required
def sesmt_editar(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)

    if request.method == 'POST':
        form = SESMTForm(request.POST, request.FILES, instance=chamado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formulário SESMT salvo com sucesso!')
            return redirect('sesmt_view')
    else:
        form = SESMTForm(instance=chamado)

    return render(request, 'formulario/sesmt_editar.html', {'form': form, 'chamado': chamado})

@login_required
def rh_dp_view(request):
    chamados = Chamado.objects.filter(assinatura_sesmt__isnull=False).exclude(assinatura_sesmt='')

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

    return render(request, 'formulario/rh_dp_editar.html', {'form_rh_dp': form_rh_dp, 'chamado': chamado})
