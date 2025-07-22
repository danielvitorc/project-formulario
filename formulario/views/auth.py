from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Verificar se o usuário tem perfil
            if not hasattr(user, 'profile'):
                from ..models import UserProfile
                UserProfile.objects.create(user=user)
            
            # Verificar se o usuário está bloqueado
            if user.profile.is_blocked:
                messages.error(request, 'Sua conta está bloqueada. Entre em contato com o administrador.')
                return render(request, 'formulario/login.html')
            
            login(request, user)
            
            # Redirecionar para tela de admin se for administrador
            if user.is_superuser or user.profile.is_admin:
                if not user.profile.is_admin:
                    user.profile.is_admin = True
                    user.profile.save()
                return redirect('admin_dashboard')
            elif user.profile.role == 'gestor':
                return redirect('gestor_view')
            elif user.profile.role == 'diretor':
                return redirect('diretor_view')
            elif user.profile.role == 'rh_dp':
                return redirect('rh_dp_view')
            elif user.profile.role == 'sesmt':
                return redirect('sesmt_view')
            else:
                messages.error(request, 'Usuário sem função definida.')
                return redirect('login')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')

    return render(request, 'formulario/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')