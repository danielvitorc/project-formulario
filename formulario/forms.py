from django import forms
from django.forms import Select
from .models import Chamado
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']  # Campos que aparecerão no formulário de cadastro


AUTORIZACOES_CHOICES = [
    ('Apto','Apto'),
    ('Não apto','Não apto'),
    ('Não aplicável','Não aplicável')
]

class GestorForm(forms.ModelForm):
    EXPOSICAO_CHOICES = [
        ('Exposição Intermitente','Exposição Intermitente'),
    ]

    NATUREZA_CHOICES = [
        ('Operações Perigosas Com Explosivos','Operações Perigosas Com Explosivos'),
        ('Operações Perigosas Com Inflamáveis','Operações Perigosas Com Inflamáveis'),
        ('Operações Perigosas Com Exposição A Roubos Ou Outras Espécies De Violência Física Nas Atividades Profissionais De Segurança Pessoal Ou Patrimonial',
         'Operações Perigosas Com Exposição A Roubos Ou Outras Espécies De Violência Física Nas Atividades Profissionais De Segurança Pessoal Ou Patrimonial'),
        ('Operações Perigosas Com Energia Elétrica','Operações Perigosas Com Energia Elétrica'),
        ('Atividades Perigosas Em Motocicleta','Atividades Perigosas Em Motocicleta'),
        ('Atividades E Operações Perigosas Com Radiações Ionizantes Ou Substâncias Radiotivas ',
         'Atividades E Operações Perigosas Com Radiações Ionizantes Ou Substâncias Radiotivas '),
    ]
    tipo_exposicao = forms.ChoiceField(
        choices =  EXPOSICAO_CHOICES,
        widget=forms.RadioSelect(), 
        required = False,
        label = 'Tipo de Exposição',
        initial='Exposição Intermitente'  
    )

    natureza_risco = forms.ChoiceField(
        choices = NATUREZA_CHOICES,
         widget=forms.Select(attrs={'class': 'natureza-select styled-form'}),
        required = False,
        label= 'Natureza do Risco'
    )

    class Meta:
        model = Chamado
        fields = [
            'nome_colaborador', 'matricula', 'funcao', 'depto', 'gestor_imediato','tipo_exposicao',
            'natureza_risco', 'descricao_atividades', 'atividade', 'locais_atuaçao', 'frequencia',
            'data_autorizacao_gestor', 'responsavel', 'assinatura_gestor' 
            ]
        widgets = {
            'data_autorizacao_gestor': forms.DateInput(attrs={'type': 'date'}),
            'descricao_atividades': forms.Textarea(attrs={'rows': 3}),
            'atividade': forms.Textarea(attrs={'rows': 3})
        }
        labels = {
            'nome_colaborador': 'Nome do Colaborador',
            'matricula': 'Matrícula',
            'funcao': 'Função',
            'depto': 'Departamento',
            'gestor_imediato': 'Gestor Imediato',
            'descricao_atividades': 'Descrição das Atividades',
            'atividade': 'Atividade',
            'locais_atuaçao': 'Locais de Atuação',
            'frequencia': 'Frequência',
            'data_autorizacao_gestor': 'Data da Autorização do Gestor',
            'responsavel': 'Responsável',
            'assinatura_gestor': 'Assinatura do Gestor',
        }

'''
class GestorUploadForm(forms.ModelForm):
    chamado_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Chamado
        fields = ['upload_gestor']

'''
    
class DiretorForm(forms.ModelForm):
    diretor_aprovacao = forms.ChoiceField(
        choices=[('', 'Selecione')] + [('True', 'Aprovado'), ('False', 'Reprovado')],
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        required=False
    )

    class Meta:
        model = Chamado
        fields = ['diretor_aprovacao', 'assinatura_diretor']


class SESMTForm(forms.ModelForm):

    aso = forms.ChoiceField(
        choices =  AUTORIZACOES_CHOICES,
        widget=forms.RadioSelect(), 
        required = False,
        label = 'ASO'
    )

    epi_epc = forms.ChoiceField(
        choices =  AUTORIZACOES_CHOICES,
        widget=forms.RadioSelect(), 
        required = False,
        label = 'EPI/EPC'
    )

    curso_nr10 = forms.ChoiceField(
        choices =  AUTORIZACOES_CHOICES,
        widget=forms.RadioSelect(), 
        required = False,
        label = 'CURSO NR-10 ATUALIZADO'
    )

    curso_sep = forms.ChoiceField(
        choices =  AUTORIZACOES_CHOICES,
        widget=forms.RadioSelect(), 
        required = False,
        label = 'CURSO SEP ATUALIZADO'
    )

    curso_nr35 = forms.ChoiceField(
        choices =  AUTORIZACOES_CHOICES,
        widget=forms.RadioSelect(), 
        required = False,
        label = 'CURSO NR-35 ATUALIZADO'
    )

    class Meta:
            model = Chamado
            fields = [
                'aso', 'aso_documento', 'aso_descricao', 'epi_epc', 'epi_epc_documento', 'epi_epc_descricao', 'curso_nr10', 'curso_nr10_documento', 'curso_sep',
                'curso_sep_documento', 'curso_sep_documento', 'curso_nr35', 'curso_nr35_documento', 'cursos_observacoes', 'data_autorizacao_sesmt', 'nome_sesmt', 'assinatura_sesmt'
                ]
            widgets = {
                'data_autorizacao_sesmt': forms.DateInput(attrs={'type': 'date'}),
                'aso_descricao': forms.Textarea(attrs={'rows': 3}),
                'epi_epc_descricao': forms.Textarea(attrs={'rows': 3}),
                'cursos_observacoes': forms.Textarea(attrs={'rows': 3}),
            }
            labels = {
               'aso' : 'ASO',
               'aso_descricao': 'Descrição',
               'epi_epc_descricao': 'Descrição',
               'cursos_observacoes': 'Observações',
               'data_autorizacao_sesmt': 'Data de autorização SESMT',
               'nome_sesmt': 'Nome',
               'assinatura_sesmt': 'Assinatura do SESMT'
            }

class RHDPForm(forms.ModelForm):

    PROCEDIMENTOS_CHOICES = [
        ('Recebido sinalização automática da autorização','Recebido sinalização automática da autorização'),
        ('Validação do relatório de comprovação via GPM','Validação do relatório de comprovação via GPM'),
        ('Registro do adicional de periculosidade','Registro do adicional de periculosidade'),
    ]

    procedimento_rh_dp = forms.ChoiceField(
        choices =  PROCEDIMENTOS_CHOICES,
        widget=forms.RadioSelect(), 
        required = False,
        label = 'REGISTRO E PROCEDIMENTOS - RH/DEPARTAMENTO PESSOAL'
    )

    class Meta:
        model = Chamado 
        fields = [
            'upload_gpm','procedimento_rh_dp', 'data_autorizacao_rh_dp', 'nome_rh_dp', 'assinatura_rh_dp'
        ]
        widgets = {
            'data_autorizacao_rh_dp': forms.DateInput(attrs={'type': 'date'}),
        }
        
        labels = {
               'data_autorizacao_rh_dp': 'Data de Autorização RH/DP',
               'nome_rh_dp': 'Nome',
               'assinatura_rh_dp': 'Assinatura  do RH/DP',
               'upload_gpm': 'Documento do GPM'
        }