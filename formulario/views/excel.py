from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment
from PIL import Image
import io
from ..models import Chamado

def preencher_excel_per(per):
    wb = load_workbook("formulario/static/per_modelo.xlsx")
    ws = wb.active

    def adicionar_imagem_excel(ws, imagem_field, celula, largura=120, altura=30):
        if imagem_field and imagem_field.name:
            try:
                img_pillow = Image.open(imagem_field)
                img_buffer = io.BytesIO()
                img_pillow.save(img_buffer, format="PNG")
                img_buffer.seek(0)

                img_excel = XLImage(img_buffer)
                img_excel.width = largura
                img_excel.height = altura
                ws.add_image(img_excel, celula)
            except Exception as e:
                print(f"Erro ao adicionar imagem em {celula}: {e}")

    ws["C5"] = per.nome_colaborador or ""
    ws["K5"] = per.matricula or ""
    ws["C6"] = per.funcao or ""
    ws["H6"] = per.depto or ""
    ws["C7"] = per.gestor_imediato or ""

    ws["B10"] = "[X]" if per.tipo_exposicao == "Exposição Intermitente" else "[  ]"

    ws["B13"] = "[X]" if per.natureza_risco == "Operações Perigosas Com Explosivos" else "[  ]"
    ws["B14"] = "[X]" if per.natureza_risco == "Operações Perigosas Com Inflamáveis" else "[  ]"
    ws["B15"] = "[X]" if per.natureza_risco == "Operações Perigosas Com Exposição A Roubos Ou Outras Espécies De Violência Física Nas Atividades Profissionais De Segurança Pessoal Ou Patrimonial" else "[  ]"
    ws["B16"] = "[X]" if per.natureza_risco == "Operações Perigosas Com Energia Elétrica" else "[  ]"
    ws["B17"] = "[X]" if per.natureza_risco == "Atividades Perigosas Em Motocicleta" else "[  ]"
    ws["B18"] = "[X]" if per.natureza_risco == "Atividades E Operações Perigosas Com Radiações Ionizantes Ou Substâncias Radiotivas" else "[  ]"

    ws["F9"] = per.descricao_atividades or ""
    ws["B20"] = (per.atividade or "").replace(';', '\n')
    ws["B19"].alignment = Alignment(wrap_text=True)
    ws["F20"] = per.locais_atuaçao or ""
    ws["J20"] = per.frequencia or ""
    ws["B22"] = per.data_autorizacao_gestor.strftime("%d/%m/%Y") if per.data_autorizacao_gestor else ""
    ws["D22"] = per.responsavel or ""

    ws["H27"] = "[X]" if per.aso == "Apto" else "[  ]"
    ws["J27"] = "[X]" if per.aso == "Não apto" else "[  ]"
    ws["K27"] = "[X]" if per.aso == "Não aplicável" else "[  ]"

    ws["B27"] = f"Observações: {per.aso_descricao}" if per.aso_descricao else "Observações:"

    ws["H30"] = "[X]" if per.epi_epc == "Apto" else "[  ]"
    ws["J30"] = "[X]" if per.epi_epc == "Não apto" else "[  ]"
    ws["K30"] = "[X]" if per.epi_epc == "Não aplicável" else "[  ]"

    ws["B30"] = f"Observações: {per.epi_epc_descricao}" if per.epi_epc_descricao else "Observações:"

    ws["H33"] = "[X]" if per.curso_nr10 == "Apto" else "[  ]"
    ws["J33"] = "[X]" if per.curso_nr10 == "Não apto" else "[  ]"
    ws["K33"] = "[X]" if per.curso_nr10 == "Não aplicável" else "[  ]"

    ws["H34"] = "[X]" if per.curso_sep == "Apto" else "[  ]"
    ws["J34"] = "[X]" if per.curso_sep == "Não apto" else "[  ]"
    ws["K34"] = "[X]" if per.curso_sep == "Não aplicável" else "[  ]"

    ws["H35"] = "[X]" if per.curso_nr35 == "Apto" else "[  ]"
    ws["J35"] = "[X]" if per.curso_nr35 == "Não apto" else "[  ]"
    ws["K35"] = "[X]" if per.curso_nr35 == "Não aplicável" else "[  ]"

    ws["B36"] = f"Observações: {per.cursos_observacoes}" if per.cursos_observacoes else "Observações:"
   
    ws["B40"] = per.data_autorizacao_sesmt.strftime("%d/%m/%Y") if per.data_autorizacao_sesmt else ""
    ws["D40"] = per.nome_sesmt or ""

    ws["B45"] = "[X]" if per.procedimento_rh_dp == "Recebido sinalização automática da autorização" else "[  ]"
    ws["B46"] = "[X]" if per.procedimento_rh_dp == "Validação do relatório de comprovação via GPM" else "[  ]"
    ws["B47"] = "[X]" if per.procedimento_rh_dp == "Registro do adicional de periculosidade" else "[  ]"

    ws["B51"] = per.data_autorizacao_rh_dp.strftime("%d/%m/%Y") if per.data_autorizacao_rh_dp else ""
    ws["D51"] = per.nome_rh_dp or ""

    # Inserção das assinaturas
    adicionar_imagem_excel(ws, per.imagem_assinatura_gestor, "J22")
    adicionar_imagem_excel(ws, per.imagem_assinatura_sesmt, "J40")
    adicionar_imagem_excel(ws, per.imagem_assinatura_rh_dp, "J51")

    # Salva em memória
    buffer = io.BytesIO()

    wb.save(buffer)
    buffer.seek(0)

    return buffer.getvalue()

@login_required
def download_per_excel(request, registro_id):
    registro = get_object_or_404(Chamado, id=registro_id)

    excel_bytes = preencher_excel_per(registro)
    nome_arquivo = f"PER_{registro.id}.xlsx"

    response = HttpResponse(
        excel_bytes,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{nome_arquivo}"'
    return response