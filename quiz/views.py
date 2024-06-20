from django.shortcuts import render, HttpResponse
from django.db.models import Count, Q
from .models import PerfilVisitante, VisitantePerguntaResposta
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from perfil_visitante.models import PerfilVisitante


from django.shortcuts import render, redirect, get_object_or_404
from .models import Pergunta, Resposta
from .forms import PerguntaForm, RespostaForm
import xlsxwriter



def criar_pergunta(request):
    if request.method == 'POST':
        form = PerguntaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_perguntas')
    else:
        form = PerguntaForm()
    
    return render(request, 'criar_pergunta.html', {'form': form})

def editar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    
    if request.method == 'POST':
        form = PerguntaForm(request.POST, instance=pergunta)
        if form.is_valid():
            form.save()
            return redirect('listar_perguntas')
    else:
        form = PerguntaForm(instance=pergunta)
    
    return render(request, 'editar_pergunta.html', {'form': form, 'pergunta': pergunta})

def criar_resposta(request):
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_respostas')
    else:
        form = RespostaForm()
    
    return render(request, 'criar_resposta.html', {'form': form})

def editar_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, id=resposta_id)
    
    if request.method == 'POST':
        form = RespostaForm(request.POST, instance=resposta)
        if form.is_valid():
            form.save()
            return redirect('listar_respostas')
    else:
        form = RespostaForm(instance=resposta)
    
    return render(request, 'editar_resposta.html', {'form': form, 'resposta': resposta})



def relatorio_completo(request):
    # Quantidade de visitantes
    total_visitantes = PerfilVisitante.objects.count()

    # Quantidade de respostas corretas e incorretas
    total_acertos = VisitantePerguntaResposta.objects.filter(resposta__correta=True).count()
    total_erros = VisitantePerguntaResposta.objects.filter(resposta__correta=False).count()

    # Respostas mais acertadas
    respostas_acertadas = VisitantePerguntaResposta.objects.values('resposta__texto_resposta').annotate(total=Count('id')).order_by('-total')[:5]

    # Cidades que mais acertaram
    cidades_acertos = PerfilVisitante.objects.values('municipio_escola').annotate(total_acertos=Count(
        'visitanteperguntaresposta', filter=Q(visitanteperguntaresposta__resposta__correta=True))).order_by('-total_acertos')[:5]

    # Notas mais dadas
    notas_mais_dadas = PerfilVisitante.objects.values('nota_visita').annotate(total=Count('id')).order_by('-total')[:5]

    # Idades mais visitadas
    idades_mais_visitadas = PerfilVisitante.objects.values('idade').annotate(total=Count('id')).order_by('-total')[:5]

    context = {
        'total_visitantes': total_visitantes,
        'total_acertos': total_acertos,
        'total_erros': total_erros,
        'respostas_acertadas': respostas_acertadas,
        'cidades_acertos': cidades_acertos,
        'notas_mais_dadas': notas_mais_dadas,
        'idades_mais_visitadas': idades_mais_visitadas,
    }

    if request.GET.get('export') == 'excel':
        response = exportar_para_excel(context)
        return response
    else:
        return render(request, 'relatorio_completo.html', context)

def exportar_para_excel(context):
    workbook = xlsxwriter.Workbook('relatorio_promar.xlsx')
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    # Escrever cabeçalhos
    headers = ['Categoria', 'Valor']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, bold)

    # Escrever dados
    row = 1
    worksheet.write(row, 0, 'Total de Visitantes')
    worksheet.write(row, 1, context['total_visitantes'])
    row += 1
    worksheet.write(row, 0, 'Total de Acertos')
    worksheet.write(row, 1, context['total_acertos'])
    row += 1
    worksheet.write(row, 0, 'Total de Erros')
    worksheet.write(row, 1, context['total_erros'])
    row += 2

    worksheet.write(row, 0, 'Respostas Mais Acertadas', bold)
    row += 1
    worksheet.write(row, 0, 'Resposta')
    worksheet.write(row, 1, 'Total')
    row += 1
    for resposta in context['respostas_acertadas']:
        worksheet.write(row, 0, resposta['resposta__texto_resposta'])
        worksheet.write(row, 1, resposta['total'])
        row += 1
    row += 1

    worksheet.write(row, 0, 'Cidades com Melhor Desempenho', bold)
    row += 1
    worksheet.write(row, 0, 'Cidade')
    worksheet.write(row, 1, 'Total de Acertos')
    row += 1
    for cidade in context['cidades_acertos']:
        worksheet.write(row, 0, cidade['municipio_escola'])
        worksheet.write(row, 1, cidade['total_acertos'])
        row += 1
    row += 1

    worksheet.write(row, 0, 'Notas Mais Dadas', bold)
    row += 1
    worksheet.write(row, 0, 'Nota')
    worksheet.write(row, 1, 'Total')
    row += 1
    for nota in context['notas_mais_dadas']:
        worksheet.write(row, 0, nota['nota_visita'])
        worksheet.write(row, 1, nota['total'])
        row += 1
    row += 1

    worksheet.write(row, 0, 'Idades Mais Visitadas', bold)
    row += 1
    worksheet.write(row, 0, 'Idade')
    worksheet.write(row, 1, 'Total')
    row += 1
    for idade in context['idades_mais_visitadas']:
        worksheet.write(row, 0, idade['idade'])
        worksheet.write(row, 1, idade['total'])
        row += 1

    workbook.close()

    # Retornar o arquivo Excel como uma resposta HTTP para download
    with open('relatorio_promar.xlsx', 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=relatorio_promar.xlsx'

    return response

