from django import forms
from django.forms import Select
from .models import Chamado
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from .models import CustomUser
from django.forms.widgets import FileInput


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

    assinar_como_gestor = forms.BooleanField(
        required=False,
        label = "Assinar como Gestor",
        help_text="Marque esta opção para assinar este formulário como gestor"
    )   

    class Meta:
        model = Chamado
        fields = [
            'nome_colaborador', 'matricula', 'funcao', 'depto', 'gestor_imediato','tipo_exposicao',
            'natureza_risco', 'descricao_atividades', 'atividade', 'locais_atuaçao', 'frequencia',
            'data_autorizacao_gestor', 'responsavel'
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
        }
        exclude = [
            'imagem_assinatura_gestor',
            'assinatura_gestor'

        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        if "assinatura_gestor" in self.fields:
            self.fields["assinatura_gestor"].widget = forms.HiddenInput()

    @staticmethod
    def generate_signature_image(name: str, cargo: str = None) -> ContentFile:

        print("Gerando assinatura para:", name, cargo)

        try:
            font_name = ImageFont.truetype("BRADHITC.TTF", 40)
            font_cargo = ImageFont.truetype("BRADHITC.TTF", 25)
            print("Fonte carregada com sucesso.")
        except IOError:
            print("Fonte não encontrada, usando padrão.")
            font_name = ImageFont.load_default()
            font_cargo = ImageFont.load_default()


        # Calcular tamanho necessário do texto
        dummy_img = Image.new('RGBA', (1, 1))
        draw_dummy = ImageDraw.Draw(dummy_img)

        bbox_name = draw_dummy.textbbox((0, 0), name, font=font_name)
        width_name = bbox_name[2] - bbox_name[0]
        height_name = bbox_name[3] - bbox_name[1]

        # Calcular tamanho do texto do cargo (se tiver)
        if cargo:
            bbox_cargo = draw_dummy.textbbox((0, 0), cargo, font=font_cargo)
            width_cargo = bbox_cargo[2] - bbox_cargo[0]
            height_cargo = bbox_cargo[3] - bbox_cargo[1]
        else:
            width_cargo = 0
            height_cargo = 0
 
        padding = 20
        img_width = max(width_name, width_cargo) + padding * 2
        img_height = height_name + height_cargo + padding * 3 

        img = Image.new('RGBA', (img_width, img_height), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Desenhar o nome no topo
        draw.text((padding, padding), name, font=font_name, fill=(0, 0, 0, 255))

        # Desenhar o cargo abaixo do nome
        if cargo:
            draw.text((padding, padding + height_name + padding // 2), cargo, font=font_cargo, fill=(0, 0, 0, 255))

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f"assinatura_{name.lower().replace(' ', '_')}.png"
        return ContentFile(buffer.getvalue(), name=filename)

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        # Converte todos os campos CharField e TextField para maiúsculas
        for field in instance._meta.get_fields():
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(instance, field.name)
                if value:
                    setattr(instance, field.name, value.upper())

        if user:
            instance.usuario = user
            nome_usuario = str(user.get_full_name() or user.username or "USUÁRIO")
            cargo_usuario = getattr(user, 'cargo', '')

            assinatura_img = self.generate_signature_image(nome_usuario, cargo_usuario)
        
        # Assinatura automática com base no tipo de usuário
        if user.role == "gestor":
            instance.assinatura_gestor = user
            instance.imagem_assinatura_gestor.save(assinatura_img.name, assinatura_img, save=False)

        elif user.role == "diretor":
            instance.assinatura_diretor = user
            instance.imagem_assinatura_diretor.save(assinatura_img.name, assinatura_img, save=False)

        elif user.role == "sesmt":
            instance.assinatura_sesmt = user
            instance.imagem_assinatura_sesmt.save(assinatura_img.name, assinatura_img, save=False)

        elif user.role == "rh_dp":
            instance.assinatura_rh_dp = user
            instance.imagem_assinatura_rh_dp.save(assinatura_img.name, assinatura_img, save=False)

        if commit:
            instance.save()
        return instance


    
class DiretorForm(forms.ModelForm):
    diretor_aprovacao = forms.ChoiceField(
        choices=[('', 'Selecione')] + [('True', 'Aprovado'), ('False', 'Reprovado')],
        widget=forms.Select(attrs={'style': 'width: 150px;'}),
        required=False
    )

    assinar_como_diretor = forms.BooleanField(
        required=False,
        label="Assinar como Diretor",
        help_text="Marque esta opção para assinar este formulário como diretor."
    )

    class Meta:
        model = Chamado
        fields = ['diretor_aprovacao']
        exclude = [
            'imagem_assinatura_diretor',
            'assinatura_diretor'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        if "assinatura_diretor" in self.fields:
            self.fields["assinatura_diretor"].widget = forms.HiddenInput()

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
    
        if user:
            instance.assinatura_diretor = user

        nome_usuario = str(user.get_full_name() or user.username or "USUÁRIO")
        cargo_usuario = getattr(user, 'cargo', '')  # pega o cargo se existir

            # Gera imagem da assinatura se desejar
        assinatura_img = GestorForm.generate_signature_image(
           nome_usuario, cargo_usuario
        )
        

        instance.imagem_assinatura_diretor.save(
            assinatura_img.name, assinatura_img, save=False
        )

        if commit:
            instance.save()
        return instance
        

        

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

    assinar_como_sesmt = forms.BooleanField(
        required=False,
        label="Assinar como SESMT",
        help_text="Marque esta opção para assinar este formulário como SESMT.",
    )

    class Meta:
            model = Chamado
            fields = [
                'aso', 'aso_documento', 'aso_descricao', 'epi_epc', 'epi_epc_documento', 'epi_epc_descricao', 'curso_nr10', 'curso_nr10_documento', 'curso_sep',
                'curso_sep_documento', 'curso_sep_documento', 'curso_nr35', 'curso_nr35_documento', 'cursos_observacoes', 'data_autorizacao_sesmt', 'nome_sesmt',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_sesmt
        if "assinatura_sesmt" in self.fields:
            self.fields["assinatura_sesmt"].widget = forms.HiddenInput()

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            instance.assinatura_sesmt = user

            nome_usuario = str(user.get_full_name() or user.username or "USUÁRIO")
            cargo_usuario = getattr(user, 'cargo', '')  # pega o cargo se existir

                # Gera imagem da assinatura se desejar
            assinatura_img = GestorForm.generate_signature_image(
            nome_usuario, cargo_usuario
            )

            instance.imagem_assinatura_sesmt.save(
                assinatura_img.name, assinatura_img, save=False
            )

        if commit:
            instance.save()
        return instance

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

    assinar_como_rh_dp = forms.BooleanField(
        required=False,
        label="Assinar como RH/DP",
        help_text="Marque esta opção para assinar este formulário como RH/DP.",
    )

    class Meta:
        model = Chamado 
        fields = [
            'upload_gpm','procedimento_rh_dp', 'data_autorizacao_rh_dp', 'nome_rh_dp'
        ]
        widgets = {
            'data_autorizacao_rh_dp': forms.DateInput(attrs={'type': 'date'}),
            'upload_gpm': FileInput(),  # Substitui o ClearableFileInput
        }
        
        labels = {
               'data_autorizacao_rh_dp': 'Data de Autorização RH/DP',
               'nome_rh_dp': 'Nome',
               'upload_gpm': 'Documento do GPM'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta o campo assinatura_diretor
        if "assinatura_rh_dp" in self.fields:
            self.fields["assinatura_rh_dp"].widget = forms.HiddenInput()

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            instance.assinatura_rh_dp = user

            nome_usuario = str(user.get_full_name() or user.username or "USUÁRIO")
            cargo_usuario = getattr(user, 'cargo', '')  # pega o cargo se existir

                # Gera imagem da assinatura se desejar
            assinatura_img = GestorForm.generate_signature_image(
            nome_usuario, cargo_usuario
            )
            instance.imagem_assinatura_rh_dp.save(
                assinatura_img.name, assinatura_img, save=False
            )

        if commit:
            instance.save()
        return instance