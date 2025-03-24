from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ChamadoForm
import io
from docx import Document

def cadastrar_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save()  # Salva no banco
            docx_content = preencher_docx(chamado)

            # Retorna o documento Word para download
            response = HttpResponse(docx_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="chamado_{chamado.id}.docx"'
            return response

    else:
        form = ChamadoForm()

    return render(request, 'formulario/chamado.html', {'form': form})


def marcar_opcao_lado_a_lado(paragrafo, valor_escolhido, opcoes):
    """
    Substitui a opção correta em casos onde as opções estão lado a lado no Word, como:
    
        Apto        Não apto        Não aplicável
        [  ]        [  ]            [  ]
    
    Se 'Apto' for selecionado no formulário, fica assim:
    
        Apto        Não apto        Não aplicável
        [X]        [  ]            [  ]
    """
    
    texto_original = paragrafo.text  # Guarda o texto original para debug
    print(f"Antes: {texto_original}")  # TESTE DEBUG

    # Criar uma cópia da string para modificar
    novo_texto = texto_original

    # Encontra a posição da opção selecionada
    for i, opcao in enumerate(opcoes):
        if opcao.lower() == valor_escolhido.lower():  # Ignora maiúsculas e minúsculas
            # Substituir apenas o primeiro "[  ]" encontrado
            partes = novo_texto.split("[  ]")
            if len(partes) > i + 1:  # Garante que a opção existe
                partes[i + 1] = "[X]" + partes[i + 1]  # Marca apenas a opção escolhida
                novo_texto = "[  ]".join(partes)

    print(f"Depois: {novo_texto}")  # TESTE DEBUG
    paragrafo.text = novo_texto  # Atualiza o texto do parágrafo no Word


def preencher_docx(chamado):
    # Caminho do modelo Word

    # Carrega o modelo
    doc = Document('formulario/static/modelo.docx')

    def marcar_opcao(texto, valor_escolhido, opcoes):
        """
        Substitui uma lista de opções do Word por uma versão onde apenas a escolhida está marcada.
        Exemplo:
            "[ ] Apto" -> "[X] Apto" (se 'Apto' for o valor escolhido)
        """
        for opcao in opcoes:
            if opcao == valor_escolhido:
                texto = texto.replace(f"[ ] {opcao}", f"[X] {opcao}")
            else:
                texto = texto.replace(f"[ ] {opcao}", f"[ ] {opcao}")
        return texto


    # Substitui os placeholders pelos valores do chamado
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
        "{{tipo_parecer}}": chamado.tipo_parecer,
        "{{area_risco}}": chamado.area_risco,
        "{{aso}}": chamado.aso,
        "{{treinamentoa}}": chamado.treinamentoa,
        "{{nao_registrado}}": chamado.nao_registrado,
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



        
    }

    # Substituir texto em parágrafos
    for paragrafo in doc.paragraphs:
        for chave, valor in placeholders.items():
            if chave in paragrafo.text:
                for run in paragrafo.runs:
                    run.text = run.text.replace(chave, valor)

    # Substituir dentro das tabelas
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for paragrafo in celula.paragraphs:
                    for chave, valor in placeholders.items():
                        if chave in paragrafo.text:
                            for run in paragrafo.runs:
                                run.text = run.text.replace(chave, valor)

    for paragrafo in doc.paragraphs:
        if "Tipo de Parecer:" in paragrafo.text:
            paragrafo.text = marcar_opcao(paragrafo.text, chamado.tipo_parecer, ["Eventual", "Intermitente", "Permanente", "Sem Exposição"])

        if "Área de Risco:" in paragrafo.text:
            paragrafo.text = marcar_opcao(paragrafo.text, chamado.area_risco, ["Sim", "Não"])

        # Se o parágrafo contém as opções ASO lado a lado, marcamos corretamente
        if "Apto" in paragrafo.text and "Não apto" in paragrafo.text and "Não aplicável" in paragrafo.text:
            marcar_opcao_lado_a_lado(paragrafo, chamado.aso, ["Apto", "Não apto", "Não aplicável"])

        # Se o parágrafo contém as opções Treinamento lado a lado, marcamos corretamente
        if "Treinamento" in paragrafo.text and "Apto" in paragrafo.text:
            marcar_opcao_lado_a_lado(paragrafo, chamado.treinamentoa, ["Apto", "Não apto", "Não aplicável"])

    # Substituir dentro das tabelas (para garantir que funcione também em tabelas)
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for paragrafo in celula.paragraphs:
                    if "Apto" in paragrafo.text and "Não apto" in paragrafo.text and "Não aplicável" in paragrafo.text:
                        marcar_opcao_lado_a_lado(paragrafo, chamado.aso, ["Apto", "Não apto", "Não aplicável"])

                    if "Treinamento" in paragrafo.text and "Apto" in paragrafo.text:
                        marcar_opcao_lado_a_lado(paragrafo, chamado.treinamentoa, ["Apto", "Não apto", "Não aplicável"])

    # Salva o documento preenchido em memória

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return buffer.getvalue()
