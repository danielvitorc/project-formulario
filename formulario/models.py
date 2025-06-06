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
    "3feef40d62e9a74915b39abafad145bf5b34bd7e1955694dacbe6690fe9301b7"
]

HASHES_ASSINATURAS_DIRETORES = [
    "dcad43271bb1a067f3c44954e39e9456d8970a0822416a9d0df7702c6437d63e",
    "f4df4acbfe24928104732011da7a60c5c8b50f7a9a27ae41c78f22e57354b0f6",
    "c86198dc67fb0fb44fed3215f02774018afebc923ad4ebb1cf05d6c672e678ae"

]

HASHES_ASSINATURAS_SESMT = [
    "4fa8760fd175c47be450e4bdffdd4652f8b4fa6d62a328535746015af373f83d"
]

HASHES_ASSINATURAS_RH_DP = [
    "d22bffc2826652252094f1edbf320b1802a0d542f6740fe11eca998d684a7694"
]  

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
    atividade = models.TextField()
    locais_atuaçao = models.CharField(max_length=255)
    frequencia = models.CharField(max_length=50)
    data_autorizacao_gestor = models.DateField()
    responsavel = models.CharField(max_length=100)
    assinatura_gestor = models.ImageField(upload_to="assinaturas/gestor/chamado")
    
    upload_gestor = models.FileField(upload_to='registros/uploads', null=True, blank=True)

    # Campo cadastrado pelo Diretor
    diretor_aprovacao = models.BooleanField(null=True, blank=True)
    assinatura_diretor = models.ImageField(upload_to="assinaturas/diretor/chamado", null=True, blank=True)

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

        if self.assinatura_diretor and hasattr(self.assinatura_diretor, 'file'):
            try:
                self.assinatura_diretor.file.seek(0)
                hash_diretor = hashlib.sha256(self.assinatura_diretor.file.read()).hexdigest()
                self.assinatura_diretor.file.seek(0)
            except Exception:
                raise ValidationError("Não foi possível processar o arquivo de assinatura do diretor")
            
            if hash_diretor not in HASHES_ASSINATURAS_DIRETORES:
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

    def get_status_diretor(self):
        if self.diretor_aprovacao == True:
            return '✔️ Aprovado'
        elif self.diretor_aprovacao == False:
            return '❌ Reprovado'
        else:
            return '⏳ Pendente'
