from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import ChamadoForm
import io
from docx import Document

# View de Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_user_by_role(user)
        else:
            return HttpResponse("Credenciais inválidas")
    return render(request, 'formulario/login.html')

# Redirecionamento por tipo de usuário
def redirect_user_by_role(user):
    if user.role == 'gestor':
        return redirect('cadastrar_chamado')
    elif user.role == 'diretor':
        return redirect('cadastrar_chamado')
    return redirect('cadastrar_chamado')


@login_required
def diretor_dashboard(request):
    return HttpResponse("Bem-vindo, Diretor!")



def cadastrar_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)  # Não salva no banco ainda

            # Se a autorização não for "Autorizado", limpa o campo "credenciado_a"
            if chamado.autorizacao != "Autorizado":
                chamado.credenciado_a = ""

            chamado.save()  # Agora salva no banco

            # Gerar o documento Word atualizado
            docx_content = preencher_docx(chamado)

            # Retorna o documento Word para download
            response = HttpResponse(docx_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="chamado_{chamado.id}.docx"'
            return response

    else:
        form = ChamadoForm()

    return render(request, 'formulario/chamado.html', {'form': form})

def preencher_docx(chamado):

    # Carrega o modelo do Word
    doc = Document('formulario/static/modelo.docx')

    # Se não for autorizado, o campo "credenciado_a" fica vazio
    credenciado_a_texto = chamado.credenciado_a if chamado.autorizacao == "Autorizado" else ""

    # Define os valores para os campos de autorização
    autorizacao_sim = "X" if chamado.autorizacao == "Autorizado" else ""
    autorizacao_nao = "X" if chamado.autorizacao == "Nao Autorizado" else ""

    # Define os valores para os campos de risco
    risco_sim = "X" if chamado.area_risco == "Sim" else ""
    risco_nao = "X" if chamado.area_risco == "Não" else ""

    # Dicionário com os placeholders e seus valores correspondentes
    placeholders = {
        "{{nome}}": chamado.nome,
        "{{matricula}}": chamado.matricula,
        "{{funcao}}": chamado.funcao,
        "{{depto}}": chamado.depto,
        "{{n_chamado}}": chamado.n_chamado,
        "{{atividade}}": chamado.atividade,
        "{{areas}}": chamado.areas,
        "{{frequencia}}": chamado.frequencia,
        "{{data}}": chamado.data.strftime("%d/%m/%Y") if chamado.data else "",
        "{{laudo}}": chamado.laudo,
        "{{area_risco}}": chamado.area_risco,
        "{{aso}}": chamado.aso,
        "{{treinamentoa}}": chamado.treinamentoa,
        "{{nome2}}": chamado.nome2 or "",
        "{{data2}}": chamado.data2.strftime("%d/%m/%Y") if chamado.data2 else "",
        "{{nome3}}": chamado.nome3 or "",
        "{{data3}}": chamado.data3.strftime("%d/%m/%Y") if chamado.data3 else "",
        "{{nome4}}": chamado.nome4 or "",
        "{{data4}}": chamado.data4.strftime("%d/%m/%Y") if chamado.data4 else "",
        "{{nome5}}": chamado.nome5 or "",
        "{{data5}}": chamado.data5.strftime("%d/%m/%Y") if chamado.data5 else "",
        "{{nome6}}": chamado.nome6 or "",
        "{{data6}}": chamado.data6.strftime("%d/%m/%Y") if chamado.data6 else "",
        "{{autorizacaosim}}": autorizacao_sim,
        "{{autorizacaonao}}": autorizacao_nao,
        "{{credenciado_a}}": credenciado_a_texto,
        "{{riscosim}}": risco_sim,
        "{{risconao}}": risco_nao,
    }

    # Substituir valores nos parágrafos
    for paragrafo in doc.paragraphs:
        for chave, valor in placeholders.items():
            if chave in paragrafo.text:
                paragrafo.text = paragrafo.text.replace(chave, valor)

    # Substituir dentro das tabelas (caso os checkboxes estejam lá)
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for paragrafo in celula.paragraphs:
                    for chave, valor in placeholders.items():
                        if chave in paragrafo.text:
                            paragrafo.text = paragrafo.text.replace(chave, valor)

    # Salva o documento preenchido em memória
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer.getvalue()