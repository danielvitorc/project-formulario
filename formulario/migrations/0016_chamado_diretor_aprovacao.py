# Generated by Django 5.1.7 on 2025-06-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0015_alter_chamado_natureza_risco'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='diretor_aprovacao',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
