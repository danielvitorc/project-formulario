from django import forms
from .models import Chamado

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'data2': forms.DateInput(attrs={'type': 'date'}),
            'data3': forms.DateInput(attrs={'type': 'date'}),
            'data4': forms.DateInput(attrs={'type': 'date'}),
            'data5': forms.DateInput(attrs={'type': 'date'}),
            'data6': forms.DateInput(attrs={'type': 'date'}),
            'area_risco': forms.Select(choices=Chamado.AREA_RISCO_CHOICES),
            'autorizacao': forms.Select(choices=Chamado.AUTORIZACAO_CHOICES, attrs={'id': 'id_autorizacao'}),
            'credenciado_a': forms.TextInput(attrs={'id': 'id_credenciado_a', 'style': 'display:none;'}),
        }
