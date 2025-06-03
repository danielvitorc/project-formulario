from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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

def logout_view(request):
    logout(request)
    return redirect('login')