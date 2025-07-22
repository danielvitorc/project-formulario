from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from ..admin_models import UserProfile, ActivityLog
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()

def log_activity(user, action):
    """Registra atividade do usuário"""
    ActivityLog.objects.create(user=user, action=action)

# Decorator para verificar se o usuário é admin
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Verificar se o usuário tem perfil
        if not hasattr(request.user, 'profile'):
            UserProfile.objects.create(user=request.user)
        
        # Permitir acesso para superusuários ou administradores
        if not (request.user.is_superuser or request.user.profile.is_admin):
            messages.error(request, 'Acesso negado. Você não tem permissão de administrador.')
            return redirect('login')
        
        # Se for superusuário mas não tem is_admin marcado, marcar automaticamente
        if request.user.is_superuser and not request.user.profile.is_admin:
            request.user.profile.is_admin = True
            request.user.profile.save()
            
        return view_func(request, *args, **kwargs)
    return wrapper
@admin_required
def admin_dashboard(request):
    """Dashboard principal do administrador"""
    total_usuarios = User.objects.count()
    usuarios_bloqueados = UserProfile.objects.filter(is_blocked=True).count()
    usuarios_admin = UserProfile.objects.filter(is_admin=True).count()
    usuarios_ativos = User.objects.filter(is_active=True).count()
    
    # Resumo de Atividades
    atividades_recentes = ActivityLog.objects.all().order_by("-timestamp")[:10] # Últimas 10 atividades
    
    context = {
        'total_usuarios': total_usuarios,
        'usuarios_bloqueados': usuarios_bloqueados,
        'usuarios_admin': usuarios_admin,
        'usuarios_ativos': usuarios_ativos,
        'atividades_recentes': atividades_recentes,
    }
    return render(request, 'formulario/admin/dashboard.html', context)

@admin_required
def admin_usuarios(request):
    """Lista todos os usuários para gerenciamento"""
    usuarios = User.objects.all().order_by('username')
    return render(request, 'formulario/admin/usuarios.html', {'usuarios': usuarios})

class AdminUserCreationForm(UserCreationForm):
    """Formulário customizado para criação de usuários pelo admin"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    cargo = forms.CharField(max_length=100, required=False, label='Cargo')
    role = forms.ChoiceField(
        choices=[('', 'Selecione...')] + User.ROLE_CHOICES,
        required=False,
        label='Função'
    )
    is_admin = forms.BooleanField(required=False, label='É Administrador')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'cargo', 'role', 'password1', 'password2')

@admin_required
def admin_criar_usuario(request):
    """Criar novo usuário"""
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Criar ou atualizar perfil
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.is_admin = form.cleaned_data.get('is_admin', False)
            profile.role = form.cleaned_data.get('role')
            profile.save()
            
            messages.success(request, f'Usuário {user.username} criado com sucesso!')
            log_activity(request.user, f'Criou o usuário {user.username}')
            return redirect('admin_usuarios')
    else:
        form = AdminUserCreationForm()
    
    return render(request, 'formulario/admin/criar_usuario.html', {'form': form})

@admin_required
def admin_editar_usuario(request, user_id):
    """Editar usuário existente"""
    usuario = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Atualizar dados básicos
        usuario.first_name = request.POST.get('first_name', '')
        usuario.last_name = request.POST.get('last_name', '')
        usuario.email = request.POST.get('email', '')
        usuario.cargo = request.POST.get('cargo', '')
        profile, created = UserProfile.objects.get_or_create(user=usuario)
        profile.role = request.POST.get('role', '')
        usuario.is_active = 'is_active' in request.POST
        usuario.save()
        
        # Atualizar perfil
        profile, created = UserProfile.objects.get_or_create(user=usuario)
        profile.is_admin = 'is_admin' in request.POST
        profile.is_blocked = 'is_blocked' in request.POST
        profile.save()
        
        messages.success(request, f'Usuário {usuario.username} atualizado com sucesso!')
        log_activity(request.user, f'Atualizou o usuário {usuario.username}')
        return redirect('admin_usuarios')
    
    return render(request, 'formulario/admin/editar_usuario.html', {'usuario': usuario})

@admin_required
def admin_trocar_senha(request, user_id):
    """Trocar senha de um usuário"""
    usuario = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if nova_senha and nova_senha == confirmar_senha:
            if len(nova_senha) >= 8:
                usuario.set_password(nova_senha)
                usuario.save()
                messages.success(request, f'Senha do usuário {usuario.username} alterada com sucesso!')
                log_activity(request.user, f'Alterou a senha do usuário {usuario.username}')
                return redirect('admin_usuarios')
            else:
                messages.error(request, 'A senha deve ter pelo menos 8 caracteres.')
        else:
            messages.error(request, 'As senhas não coincidem.')
    
    return render(request, 'formulario/admin/trocar_senha.html', {'usuario': usuario})

@admin_required
def admin_bloquear_usuario(request, user_id):
    """Bloquear/desbloquear usuário"""
    usuario = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=usuario)
    
    # Não permitir que o admin se bloqueie
    if usuario == request.user:
        messages.error(request, 'Você não pode bloquear sua própria conta.')
        return redirect('admin_usuarios')
    
    profile.is_blocked = not profile.is_blocked
    profile.save()
    
    status = 'bloqueado' if profile.is_blocked else 'desbloqueado'
    messages.success(request, f'Usuário {usuario.username} {status} com sucesso!')
    log_activity(request.user, f'{status.capitalize()} o usuário {usuario.username}')
    return redirect('admin_usuarios')

@admin_required
def admin_excluir_usuario(request, user_id):
    """Excluir usuário"""
    usuario = get_object_or_404(User, id=user_id)
    
    # Não permitir que o admin se exclua
    if usuario == request.user:
        messages.error(request, 'Você não pode excluir sua própria conta.')
        return redirect('admin_usuarios')
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuário {username} excluído com sucesso!')
        log_activity(request.user, f'Excluiu o usuário {username}')
        return redirect('admin_usuarios')
    
    return render(request, 'formulario/admin/confirmar_exclusao.html', {'usuario': usuario})

