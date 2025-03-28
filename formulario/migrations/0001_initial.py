# Generated by Django 5.1.7 on 2025-03-24 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chamado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('matricula', models.CharField(max_length=50)),
                ('funcao', models.CharField(max_length=255)),
                ('depto', models.CharField(max_length=255)),
                ('numero_chamado', models.CharField(max_length=50)),
                ('atividade', models.TextField()),
                ('areas_operacionais_com_risco', models.TextField()),
                ('frequencia', models.IntegerField()),
                ('data_criacao', models.DateField()),
                ('nome1', models.CharField(max_length=255)),
                ('data1', models.DateField()),
                ('nome2', models.CharField(blank=True, max_length=255, null=True)),
                ('data2', models.DateField(blank=True, null=True)),
                ('nome3', models.CharField(blank=True, max_length=255, null=True)),
                ('data3', models.DateField(blank=True, null=True)),
                ('nome4', models.CharField(blank=True, max_length=255, null=True)),
                ('data4', models.DateField(blank=True, null=True)),
                ('nome5', models.CharField(blank=True, max_length=255, null=True)),
                ('data5', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
