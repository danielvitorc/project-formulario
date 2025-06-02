from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import hashlib


# Modelo de Usuário Customizado
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('gestor', 'Gestor'),
        ('diretor', 'Diretor'),
        ('rh_dp', 'RH/DP'),
        ('sesmt','Sesmt')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)

HASHES_ASSINATURAS_GESTORES = [
    "bc61c2c356167b859d9a008035e841ee32236ad44356772bfd5cec4cde5b3ffc"
]
HASHES_ASSINATURAS_SESMT = [
    "ec8ff0a6954a5f54e4ad246f0a788d076f675e457bca16a04248718cca3fe631"
]

HASHES_ASSINATURAS_RH_DP = [
    "8e551767cfe9d662f0185cff3840c4616401a3726f52898ee38857cf495cbb8f"
]  

class Chamado(models.Model):

    # Campos cadastrados pelo Gestor
    nome_colaborador = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50)
    funcao = models.CharField(max_length=100)
    depto = models.CharField(max_length=100)
    gestor_imediato = models.CharField(max_length=100)
    tipo_exposicao = models.CharField(max_length=100)
    natureza_risco = models.CharField(max_length=100)
    outro_natureza_risco = models.CharField(max_length=100, null=True, blank=True)
    descricao_atividades = models.TextField()
    atividade = models.TextField()
    locais_atuaçao = models.CharField(max_length=255)
    frequencia = models.CharField(max_length=50)
    data_autorizacao_gestor = models.DateField()
    responsavel = models.CharField(max_length=100)
    assinatura_gestor = models.ImageField(upload_to="assinaturas/gestor/chamado")
    
    upload_gestor = models.FileField(upload_to='registros/uploads', null=True, blank=True)

    # Campo cadastrado pelo Diretor
    diretor_aprovacao = models.BooleanField(default=False, null=True, blank=True)

    # Campos cadastrados pelo SESMT
    aso = models.CharField(max_length=100, null=True, blank=True)
    aso_descricao = models.TextField(max_length=100, blank=True, null=True)
    epi_epc = models.CharField(max_length=100,blank=True, null=True)
    epi_epc_descricao = models.CharField(max_length=100, blank=True, null=True)
    curso_nr10 = models.CharField(max_length=100,blank=True, null=True)
    curso_sep = models.CharField(max_length=100,blank=True, null=True)
    curso_nr35 = models.CharField(max_length=100,blank=True, null=True)
    cursos_observacoes = models.TextField(blank=True, null=True)
    data_autorizacao_sesmt = models.DateField(null=True, blank=True)
    nome_sesmt = models.CharField(max_length=100, null=True, blank=True)

    assinatura_sesmt = models.ImageField(upload_to="assinaturas/sesmt/chamado")

    # Campos cadastrados pelo RH/DP
    procedimento_rh_dp = models.CharField(max_length=100, null=True, blank=True)
    data_autorizacao_rh_dp = models.DateField(null=True, blank=True)
    nome_rh_dp = models.CharField(max_length=100, null=True, blank=True)
    assinatura_rh_dp =  models.ImageField(upload_to="assinaturas/rh_dp/chamado")

    def __str__(self):
        return f"{self.nome_colaborador} - {self.responsavel}"
    
    def clean(self):
        super().clean()

        if self.assinatura_gestor and hasattr(self.assinatura_gestor, 'file'):
            try:
                self.assinatura_gestor.file.seek(0)
                hash_gestor = hashlib.sha256(self.assinatura_gestor.file.read()).hexdigest()
                self.assinatura_gestor.file.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do gestor")
            
            if hash_gestor not in HASHES_ASSINATURAS_GESTORES:
                raise ValidationError("Arquivo de assinatura inválido")

        if self.assinatura_sesmt and hasattr(self.assinatura_sesmt, 'file'):
            try:
                self.assinatura_sesmt.file.seek(0)
                hash_sesmt = hashlib.sha256(self.assinatura_sesmt.file.read()).hexdigest()
                self.assinatura_sesmt.file.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do sesmt")
            
            if hash_sesmt not in HASHES_ASSINATURAS_SESMT:
                raise ValidationError("Arquivo de assinatura inválido")

        if self.assinatura_rh_dp and hasattr(self.assinatura_rh_dp, 'file'):
            try:
                self.assinatura_rh_dp.file.seek(0)
                hash_rh_dp = hashlib.sha256(self.assinatura_rh_dp.file.read()).hexdigest()
                self.assinatura_rh_dp.file.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do RH/DP")
            
            if hash_rh_dp not in HASHES_ASSINATURAS_RH_DP:
                raise ValidationError("Arquivo de assinatura inválido")
    
    def sesmt_preenchido(self):
        return bool(self.assinatura_sesmt)

    def rh_dp_preenchido(self):
        return bool(self.assinatura_rh_dp)
