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
    ws["B11"] = "[X]" if per.tipo_exposicao == "Exposição Permanente" else "[  ]"

    ws["B14"] = "[X]" if per.natureza_risco == "Risco Elétrico" else "[  ]"
    ws["B15"] = "[X]" if per.natureza_risco == "Inflamáveis" else "[  ]"
    ws["B16"] = "[X]" if per.natureza_risco == "Explosivos" else "[  ]"

    ws["B17"] = "[X]" if per.outro_natureza_risco else "[  ]"

    ws["C17"] = f"Outro: {per.outro_natureza_risco}" if per.outro_natureza_risco else "Outro:"

    ws["F9"] = per.descricao_atividades or ""
    ws["B19"] = (per.atividade or "").replace(';', '\n')
    ws["B19"].alignment = Alignment(wrap_text=True)
    ws["F19"] = per.locais_atuaçao or ""
    ws["J19"] = per.frequencia or ""
    ws["B21"] = per.data_autorizacao_gestor.strftime("%d/%m/%Y") if per.data_autorizacao_gestor else ""
    ws["D21"] = per.responsavel or ""

    ws["H26"] = "[X]" if per.aso == "Apto" else "[  ]"
    ws["J26"] = "[X]" if per.aso == "Não Apto" else "[  ]"
    ws["K26"] = "[X]" if per.aso == "Não aplicável" else "[  ]"

    ws["B26"] = f"Observações: {per.aso_descricao}" if per.aso_descricao else "Observações:"

    ws["H29"] = "[X]" if per.epi_epc == "Apto" else "[  ]"
    ws["J29"] = "[X]" if per.epi_epc == "Não Apto" else "[  ]"
    ws["K29"] = "[X]" if per.epi_epc == "Não aplicável" else "[  ]"

    ws["B29"] = f"Observações: {per.epi_epc_descricao}" if per.epi_epc_descricao else "Observações:"

    ws["H32"] = "[X]" if per.curso_nr10 == "Apto" else "[  ]"
    ws["J32"] = "[X]" if per.curso_nr10 == "Não Apto" else "[  ]"
    ws["K32"] = "[X]" if per.curso_nr10 == "Não aplicável" else "[  ]"

    ws["H33"] = "[X]" if per.curso_sep == "Apto" else "[  ]"
    ws["J33"] = "[X]" if per.curso_sep == "Não Apto" else "[  ]"
    ws["K33"] = "[X]" if per.curso_sep == "Não aplicável" else "[  ]"

    ws["H34"] = "[X]" if per.curso_nr35 == "Apto" else "[  ]"
    ws["J34"] = "[X]" if per.curso_nr35 == "Não Apto" else "[  ]"
    ws["K34"] = "[X]" if per.curso_nr35 == "Não aplicável" else "[  ]"

    ws["B35"] = f"Observações: {per.cursos_observacoes}" if per.cursos_observacoes else "Observações:"
   
    ws["B39"] = per.data_autorizacao_sesmt.strftime("%d/%m/%Y") if per.data_autorizacao_sesmt else ""
    ws["D39"] = per.nome_sesmt or ""

    ws["B44"] = "[X]" if per.procedimento_rh_dp == "Recebido sinalização automática da autorização" else "[  ]"
    ws["B45"] = "[X]" if per.procedimento_rh_dp == "Validação do relatório de comprovação via GPM" else "[  ]"
    ws["B46"] = "[X]" if per.procedimento_rh_dp == "Registro do adicional de periculosidade" else "[  ]"

    ws["B50"] = per.data_autorizacao_rh_dp.strftime("%d/%m/%Y") if per.data_autorizacao_rh_dp else ""
    ws["D50"] = per.nome_rh_dp or ""

    # Inserção das assinaturas
    adicionar_imagem_excel(ws, per.assinatura_gestor, "J21")
    adicionar_imagem_excel(ws, per.assinatura_sesmt, "J39")
    adicionar_imagem_excel(ws, per.assinatura_rh_dp, "J50")

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