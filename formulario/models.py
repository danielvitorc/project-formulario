from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.timezone import now

# Modelo de Usuário Customizado
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('gestor', 'Gestor'),
        ('diretor', 'Diretor/Gerente'),
        ('rh_dp', 'RH/DP'),
        ('sesmt','Sesmt'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)

User = get_user_model()

class Chamado(models.Model):
    usuario_gestor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    # Campos cadastrados pelo Gestor
    nome_colaborador = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50)
    funcao = models.CharField(max_length=100)
    depto = models.CharField(max_length=100)
    gestor_imediato = models.CharField(max_length=100)
    tipo_exposicao = models.CharField(max_length=100)
    natureza_risco = models.CharField(max_length=255)
    descricao_atividades = models.TextField()
    locais_atuaçao = models.CharField(max_length=255)
    frequencia = models.CharField(max_length=50, default='16/06 - 15/07.')
    responsavel = models.CharField(max_length=100)
    
    # Assinatura do gestor
    assinatura_gestor =  models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='chamados_assinados_como_gestor')
    data_autorizacao_gestor = models.DateField(null=True, blank=True)
    imagem_assinatura_gestor = models.ImageField(upload_to="assinaturas/gestor/chamado", null=True, blank=True)

    # Campo cadastrado pelo Diretor
    diretor_aprovacao = models.BooleanField(null=True, blank=True)
    assinatura_diretor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='chamados_assinados_como_diretor')
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/chamado", null=True, blank=True)

    # Campos cadastrados pelo SESMT
    aso = models.CharField(max_length=100, null=True, blank=True)
    aso_documento = models.FileField(upload_to='registros/uploads', null=True, blank=True)
    aso_descricao = models.TextField(max_length=100, blank=True, null=True)
    epi_epc = models.CharField(max_length=100,blank=True, null=True)
    epi_epc_documento = models.FileField(upload_to='registros/uploads', null=True, blank=True)
    epi_epc_descricao = models.CharField(max_length=100, blank=True, null=True)
    curso_nr10 = models.CharField(max_length=100,blank=True, null=True)
    curso_nr10_documento = models.FileField(upload_to='registros/uploads', null=True, blank=True)
    curso_sep = models.CharField(max_length=100,blank=True, null=True)
    curso_sep_documento = models.FileField(upload_to='registros/uploads', null=True, blank=True)
    curso_nr35 = models.CharField(max_length=100,blank=True, null=True)
    curso_nr35_documento = models.FileField(upload_to='registros/uploads', null=True, blank=True)
    cursos_observacoes = models.TextField(blank=True, null=True)
    data_autorizacao_sesmt = models.DateField(null=True, blank=True)
    nome_sesmt = models.CharField(max_length=100, null=True, blank=True)

    assinatura_sesmt = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='chamados_assinados_como_sesmt')
    imagem_assinatura_sesmt = models.ImageField(upload_to="assinaturas/sesmt/chamado", null=True, blank=True)

    # Campos cadastrados pelo RH/DP
    upload_gpm = models.FileField(upload_to='registros/uploads', null=True, blank=True)
    procedimento_rh_dp = models.CharField(max_length=100, null=True, blank=True)
    data_autorizacao_rh_dp = models.DateField(null=True, blank=True)
    nome_rh_dp = models.CharField(max_length=100, null=True, blank=True)

    # Assinatura do RH/DP
    assinatura_rh_dp =  models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='chamados_assinados_como_rh_dp')
    imagem_assinatura_rh_dp = models.ImageField(upload_to="assinaturas/rh_dp/chamado", null=True, blank=True)

    gestor_ciente =  models.BooleanField(default=False, null=True, blank=True)
    sesmt_ciente =  models.BooleanField(default=False, null=True, blank=True)
    rh_dp_ciente =  models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.nome_colaborador} - {self.responsavel}"
    
    def assinar_gestor(self, user):
        self.assinatura_gestor = user
        self.save()

    def assinar_diretor(self, user):
        self.assinatura_diretor = user
        self.save()

    def assinar_sesmt(self, user):
        self.assinatura_sesmt = user
        self.save()

    def assinar_rh_dp(self, user):
        self.assinatura_rh_dp = user
        self.save()
    
    def sesmt_preenchido(self):
        return bool(self.assinatura_sesmt)

    def rh_dp_preenchido(self):
        return bool(self.assinatura_rh_dp)

    # Método de direcionamento de chamados excluidos para o backup
    def delete(self, *args, **kwargs):
        # Extrai user e motivo_exclusao de kwargs
        user = kwargs.pop("user", None)
        motivo_exclusao = kwargs.pop("motivo_exclusao", None)

        if not motivo_exclusao:
            raise ValueError("Motivo obrigatório para exclusão!")

        # Monta os dados do backup
        backup_data = {
            field.name: getattr(self, field.name)
            for field in self._meta.fields
            if field.name != 'id'
        }

        backup_data['data_exclusao'] = now()
        backup_data['excluido_por'] = user
        backup_data['motivo_exclusao'] = motivo_exclusao

        # Cria o backup
        from .models import ChamadoBackup
        ChamadoBackup.objects.create(**backup_data)

        # Exclui o original
        super().delete(*args, **kwargs)
    
class ChamadoBackup(models.Model):
    
    usuario_gestor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    nome_colaborador = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50)
    funcao = models.CharField(max_length=100)
    depto = models.CharField(max_length=100)
    gestor_imediato = models.CharField(max_length=100)
    tipo_exposicao = models.CharField(max_length=100)
    natureza_risco = models.CharField(max_length=255)
    descricao_atividades = models.TextField()
    locais_atuaçao = models.CharField(max_length=255)
    frequencia = models.CharField(max_length=50, default='16/06 - 15/07.')
    responsavel = models.CharField(max_length=100)

    assinatura_gestor = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,
        related_name='backup_assinados_como_gestor')
    data_autorizacao_gestor = models.DateField(null=True, blank=True)
    imagem_assinatura_gestor = models.ImageField(upload_to="assinaturas/backup/gestor/chamado", null=True, blank=True)

    diretor_aprovacao = models.BooleanField(null=True, blank=True)
    assinatura_diretor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='backup_assinados_como_diretor')
    data_autorizacao_diretor = models.DateTimeField(null=True, blank=True)
    imagem_assinatura_diretor = models.ImageField(upload_to="assinaturas/backup/diretor/chamado", null=True, blank=True)

    aso = models.CharField(max_length=100, null=True, blank=True)
    aso_documento = models.FileField(upload_to='backup/uploads', null=True, blank=True)
    aso_descricao = models.TextField(max_length=100, blank=True, null=True)
    epi_epc = models.CharField(max_length=100,blank=True, null=True)
    epi_epc_documento = models.FileField(upload_to='backup/uploads', null=True, blank=True)
    epi_epc_descricao = models.CharField(max_length=100, blank=True, null=True)
    curso_nr10 = models.CharField(max_length=100,blank=True, null=True)
    curso_nr10_documento = models.FileField(upload_to='backup/uploads', null=True, blank=True)
    curso_sep = models.CharField(max_length=100,blank=True, null=True)
    curso_sep_documento = models.FileField(upload_to='backup/uploads', null=True, blank=True)
    curso_nr35 = models.CharField(max_length=100,blank=True, null=True)
    curso_nr35_documento = models.FileField(upload_to='backup/uploads', null=True, blank=True)
    cursos_observacoes = models.TextField(blank=True, null=True)
    data_autorizacao_sesmt = models.DateField(null=True, blank=True)
    nome_sesmt = models.CharField(max_length=100, null=True, blank=True)

    assinatura_sesmt = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='backup_assinados_como_sesmt')
    imagem_assinatura_sesmt = models.ImageField(upload_to="assinaturas/backup/sesmt/chamado", null=True, blank=True)

    upload_gpm = models.FileField(upload_to='backup/uploads', null=True, blank=True)
    procedimento_rh_dp = models.CharField(max_length=100, null=True, blank=True)
    data_autorizacao_rh_dp = models.DateField(null=True, blank=True)
    nome_rh_dp = models.CharField(max_length=100, null=True, blank=True)

    assinatura_rh_dp =  models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='backup_assinados_como_rh_dp')
    imagem_assinatura_rh_dp = models.ImageField(upload_to="assinaturas/backup/rh_dp/chamado", null=True, blank=True)

    gestor_ciente =  models.BooleanField(default=False, null=True, blank=True)
    sesmt_ciente =  models.BooleanField(default=False, null=True, blank=True)
    rh_dp_ciente =  models.BooleanField(default=False, null=True, blank=True)

    # Campos adicionais para controle do backup
    motivo_exclusao = models.TextField(null=True, blank=True)  # Novo campo
    data_exclusao = models.DateTimeField(auto_now_add=True)
    excluido_por = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="chamados_excluidos")

    def __str__(self):
        return f"{self.nome_colaborador} (Backup)"
