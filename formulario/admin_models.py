from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

# ===== Modelos para Administração de Usuários =====

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    is_admin = models.BooleanField(default=False, verbose_name='É Administrador')
    is_blocked = models.BooleanField(default=False, verbose_name='Usuário Bloqueado')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - Admin: {self.is_admin} - Bloqueado: {self.is_blocked}'

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Usuário')
    action = models.CharField(max_length=255, verbose_name='Ação')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')

    def __str__(self):
        return f'{self.user.username} - {self.action} - {self.timestamp}'

    class Meta:
        verbose_name = 'Log de Atividade'
        verbose_name_plural = 'Logs de Atividades'
        ordering = ['-timestamp']

# Signal para criar automaticamente um perfil quando um usuário é criado

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)



