from django.db import models

class Chamado(models.Model):
    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50)
    funcao = models.CharField(max_length=255)
    depto = models.CharField(max_length=255)
    n_chamado = models.CharField(max_length=50)
    
    atividade = models.TextField()
    areas = models.TextField()
    frequencia = models.CharField(max_length=50)
    data = models.DateField()

    # Campos adicionais
    nome2 = models.CharField(max_length=255, blank=True, null=True)
    data2 = models.DateField(blank=True, null=True)
    nome3 = models.CharField(max_length=255, blank=True, null=True)
    data3 = models.DateField(blank=True, null=True)

    # ASO (checkboxes)
    APTO = 'Apto'
    NAO_APTO = 'Não Apto'
    NAO_APLICAVEL = 'Não Aplicável'
    ASO_CHOICES = [
        (APTO, 'Apto'),
        (NAO_APTO, 'Não Apto'),
        (NAO_APLICAVEL, 'Não Aplicável'),
    ]
    # Novos campos
    AREA_RISCO_CHOICES = [
        ('Sim', 'Sim'),
        ('Não', 'Não'),
    ]
    PARECER_CHOICES = [
        ('Eventual', 'Eventual'),
        ('Intermitente', 'Intermitente'),
        ('Permanente', 'Permanente'),
        ('Sem Exposição', 'Sem Exposição'),
    ]
    tipo_parecer = models.CharField(max_length=20, choices=PARECER_CHOICES, default='Sem Exposição')
    area_risco = models.CharField(max_length=3, choices=AREA_RISCO_CHOICES, default='Não')

    nao_registrado = models.CharField(max_length=255, blank=True, null=True)
    laudo = models.CharField(max_length=255, blank=True, null=True)
    aso = models.CharField(max_length=20, choices=ASO_CHOICES, default=NAO_APLICAVEL)

    nome4 = models.CharField(max_length=255, blank=True, null=True)
    data4 = models.DateField(blank=True, null=True)

    # Treinamento (checkboxes)
    treinamentoa = models.CharField(max_length=20, choices=ASO_CHOICES, default=NAO_APLICAVEL)

    nome5 = models.CharField(max_length=255, blank=True, null=True)
    data5 = models.DateField(blank=True, null=True)
    nome6 = models.CharField(max_length=255, blank=True, null=True)
    data6 = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.n_chamado}"
