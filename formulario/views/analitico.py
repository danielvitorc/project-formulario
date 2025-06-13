from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from ..models import Chamado

def analitico_view(request):
    return render(request, 'formulario/analitico.html')

def analitico_dados_view(request):
    chamados_por_depto = (
        Chamado.objects
        .values('depto')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    aprovacoes = {
        "gestor": Chamado.objects.exclude(assinatura_gestor='').count(),
        "diretor": Chamado.objects.exclude(assinatura_diretor='').count(),
        "sesmt": Chamado.objects.exclude(assinatura_sesmt='').count(),
        "rh_dp": Chamado.objects.exclude(assinatura_rh_dp='').count(),
    }

    chamados_por_mes = (
        Chamado.objects
        .annotate(mes=TruncMonth('data_autorizacao_gestor'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    return JsonResponse({
        'chamados_por_depto': list(chamados_por_depto),
        'aprovacoes': aprovacoes,
        'chamados_por_mes': list(chamados_por_mes),
    })