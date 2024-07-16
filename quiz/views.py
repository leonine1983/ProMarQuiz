from django.db.models import Count, Q
from .models import PerfilVisitante, VisitantePerguntaResposta
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from perfil_visitante.models import PerfilVisitante
from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pergunta, Resposta
from .forms import PerguntaForm, RespostaForm
import xlsxwriter



def criar_pergunta(request):
    if request.method == 'POST':
        form = PerguntaForm(request.POST)
        if form.is_valid():
            pergunta = form.save()      
            messages.success(request, "Pergunta criada com sucesso!")  
            return redirect('criar_resposta', pergunta_id=pergunta.id)
    else:
        form = PerguntaForm() 
    perguntas = Pergunta.objects.all()   
    return render(request, 'criar_pergunta.html', {'form': form, 'peguntas': perguntas})


def editar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)    
    if request.method == 'POST':
        form = PerguntaForm(request.POST, instance=pergunta)
        if form.is_valid():
            form.save()
            messages.success(request,  'Pergunta atualizada com sucesso!')
            return redirect('criar_pergunta')
    else:
        form = PerguntaForm(instance=pergunta)
    
    perguntas = Pergunta.objects.all()   
    return render(request, 'criar_pergunta.html', {'form': form, 'peguntas': perguntas})


def deletar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    pergunta.delete()
    messages.success(request, 'Pergunta excluída com sucesso')
    return redirect('criar_pergunta')


# RESPOSTAS

from django.urls import reverse_lazy
def criar_resposta(request, pergunta_id):
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():            
            form.instance.pergunta = Pergunta.objects.get(id = pergunta_id)
            form.save()     
            messages.success(request, 'Resposta criada com sucesso')       
            return redirect(reverse_lazy('criar_resposta', kwargs={'pergunta_id': pergunta_id}))
   
    else:
        form = RespostaForm()   
    pergunta_p = Pergunta.objects.get(id = pergunta_id)
    resposta_r = Resposta.objects.filter(pergunta = pergunta_id) 
    return render(request, 'criar_resposta.html', {'form': form, 'pergunta': pergunta_p, 'resposta':resposta_r})

def editar_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, id=resposta_id)
    
    if request.method == 'POST':
        form = RespostaForm(request.POST, instance=resposta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resposta atualizada com sucesso!!')
            return redirect('listar_respostas')
    else:
        form = RespostaForm(instance=resposta)
    
    return render(request, 'editar_resposta.html', {'form': form, 'resposta': resposta})


def deletar_resposta(request, resposta_id):
    # Obtém a resposta a ser deletada
    resposta = get_object_or_404(Resposta, id=resposta_id)

    # Deleta a resposta
    resposta.delete()

    # Obtém o ID da pergunta para redirecionamento
    pergunta_id = resposta.pergunta.id

    # Retorna para a página de criação de resposta
    messages.success(request, 'Resposta excluída com sucesso')
    return redirect('criar_resposta', pergunta_id=pergunta_id)


import calendar
import datetime
from django.http import HttpResponse
import xlsxwriter
from django.db.models import Count, Q
import calendar
import datetime


def relatorio_completo(request):
    if request.method == 'GET':
        mes = request.GET.get('mes')
        if mes:
            resposta_visitante = VisitantePerguntaResposta.objects.filter(criado_em__month=mes)     
            perfil_visitante = PerfilVisitante.objects.filter(criado_em__month=mes)  
            mes_nome = calendar.month_name[int(mes)]
        else:
            resposta_visitante = VisitantePerguntaResposta.objects.all()
            perfil_visitante = PerfilVisitante.objects.all()  
            mes_nome = calendar.month_name[datetime.datetime.now().month]

        # Quantidade de visitantes
        total_visitantes = perfil_visitante.count()

        # Quantidade de respostas corretas e incorretas
        total_acertos = resposta_visitante.filter(resposta__correta=True).count()
        total_erros = resposta_visitante.filter(resposta__correta=False).count()

        # Respostas mais acertadas
        respostas_acertadas = resposta_visitante.values('resposta__texto_resposta').annotate(total=Count('id')).order_by('-total')

        # Cidades que mais acertaram
        cidades_acertos = perfil_visitante.values('municipio_escola').annotate(total_acertos=Count(
            'Visitante_related', filter=Q(Visitante_related__resposta__correta=True))).order_by('-total_acertos')

        # Notas mais dadas
        notas_mais_dadas = perfil_visitante.values('nota_visita').annotate(total=Count('id')).order_by('-total')

        # Idades mais visitadas
        idades_mais_visitadas = perfil_visitante.values('idade').annotate(total=Count('id')).order_by('-total')

        context = {
            'total_visitantes': total_visitantes,
            'total_acertos': total_acertos,
            'total_erros': total_erros,
            'respostas_acertadas': respostas_acertadas,
            'cidades_acertos': cidades_acertos,
            'notas_mais_dadas': notas_mais_dadas,
            'idades_mais_visitadas': idades_mais_visitadas,
            'mes_nome': mes_nome,
            'mes': mes
        }

        if request.GET.get('export') == 'excel':               
            messages.success(request, 'Relatório exportado com sucesso')            
            mes = request.GET.get('mes')
            print(f'esse mes e o meu hahha {mes}')
            if mes:
                resposta_visitante = VisitantePerguntaResposta.objects.filter(criado_em__month=mes)     
                perfil_visitante = PerfilVisitante.objects.filter(criado_em__month=mes)  
                mes_nome = calendar.month_name[int(mes)]
            else:
                resposta_visitante = VisitantePerguntaResposta.objects.all()
                perfil_visitante = PerfilVisitante.objects.all()  
                mes_nome = calendar.month_name[datetime.datetime.now().month]

            if mes_nome == 'January':
                mes_nome = 'Janeiro'
            elif mes_nome == 'February':
                mes_nome = 'Fevereiro'
            elif mes_nome == 'March':
                mes_nome = 'Março'
            elif mes_nome == 'April':
                mes_nome = 'Abril'
            elif mes_nome == 'May':
                mes_nome = 'Maio'
            elif mes_nome == 'June':
                mes_nome='Junho'
            elif mes_nome == 'July':
                mes_nome='Julho'
            elif mes_nome == 'August':
                mes_nome='Agosto'
            elif mes_nome == 'September':
                mes_nome='Setembro'
            elif mes_nome == 'October':
                mes_nome='Outubro'
            elif mes_nome == 'November':
                mes_nome='Novembro'
            else:
                mes_nome='Dezembro'


            # Quantidade de visitantes
            total_visitantes = perfil_visitante.count()

            # Quantidade de respostas corretas e incorretas
            total_acertos = resposta_visitante.filter(resposta__correta=True).count()
            total_erros = resposta_visitante.filter(resposta__correta=False).count()

            # Respostas mais acertadas
            respostas_acertadas = resposta_visitante.values('resposta__texto_resposta').annotate(total=Count('id')).order_by('-total')

            # Cidades que mais acertaram
            cidades_acertos = perfil_visitante.values('municipio_escola').annotate(total_acertos=Count(
                'Visitante_related', filter=Q(Visitante_related__resposta__correta=True))).order_by('-total_acertos')

            # Notas mais dadas
            notas_mais_dadas = perfil_visitante.values('nota_visita').annotate(total=Count('id')).order_by('-total')

            # Idades mais visitadas
            idades_mais_visitadas = perfil_visitante.values('idade').annotate(total=Count('id')).order_by('-total')

            context = {
                'total_visitantes': total_visitantes,
                'total_acertos': total_acertos,
                'total_erros': total_erros,
                'respostas_acertadas': respostas_acertadas,
                'cidades_acertos': cidades_acertos,
                'notas_mais_dadas': notas_mais_dadas,
                'idades_mais_visitadas': idades_mais_visitadas,
                'mes_nome': mes_nome
            }

            response = exportar_para_excel(context)            
            return response            
        else:                    
            return render(request, 'relatorio_completo.html', context)
        

import xlsxwriter

def exportar_para_excel(context):
    # Inicializa o workbook e worksheet
    workbook = xlsxwriter.Workbook('relatorio_promar.xlsx')
    worksheet = workbook.add_worksheet()

    # Definindo formatos
    bold = workbook.add_format({'bold': True})
    normal = workbook.add_format()

    # Ajustes de estilo para se assemelhar ao Windows 11/12
    worksheet.set_default_row(20)  # Altura padrão das linhas
    worksheet.set_column('A:B', 20)  # Largura padrão das colunas

    # Formato para cabeçalhos
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#F2F2F2',  # Cor de fundo cinza claro
        'border': 1  # Borda fina ao redor
    })

    # Escrever cabeçalhos
    headers = ['Categoria', 'Valor']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)

    # Escrever dados usando o contexto recebido
    row = 1
    col=2
    data_format = workbook.add_format({
        'align': 'left',
        'valign': 'vcenter',
        'border': 1  # Borda fina ao redor
    })

    # Dados individuais
    worksheet.write(row, 0, "Mês", data_format)
    worksheet.write(row, 1, context['mes_nome'], data_format)
    row += 1    
    worksheet.write(row, 0, 'Total de Visitantes', data_format)
    worksheet.write(row, 1, context['total_visitantes'], data_format)
    row += 1
    worksheet.write(row, 0, 'Total de Acertos', data_format)
    worksheet.write(row, 1, context['total_acertos'], data_format)
    row += 1
    worksheet.write(row, 0, 'Total de Erros', data_format)
    worksheet.write(row, 1, context['total_erros'], data_format)
    row += 2

    # Títulos secundários
    secondary_title_format = workbook.add_format({
        'bold': True,
        'align': 'left',
        'valign': 'vcenter',
        'fg_color': '#D9EAD3',  # Cor de fundo verde claro
        'border': 1  # Borda fina ao redor
    })

    # Respostas mais acertadas
    worksheet.write(row, 0, 'Respostas Mais Acertadas', secondary_title_format)
    row += 1
    worksheet.write(row, 0, 'Resposta', header_format)
    worksheet.write(row, 1, 'Total', header_format)
    row += 1
    for resposta in context['respostas_acertadas']:
        worksheet.write(row, 0, resposta['resposta__texto_resposta'], data_format)
        worksheet.write(row, 1, resposta['total'], data_format)
        row += 1
    row += 1

    # Cidades com melhor desempenho
    worksheet.write(row, 0, 'Cidades com Melhor Desempenho', secondary_title_format)
    row += 1
    worksheet.write(row, 0, 'Cidade', header_format)
    worksheet.write(row, 1, 'Total de Acertos', header_format)
    row += 1
    for cidade in context['cidades_acertos']:
        worksheet.write(row, 0, cidade['municipio_escola'], data_format)
        worksheet.write(row, 1, cidade['total_acertos'], data_format)
        row += 1
    row += 1

    # Notas mais dadas
    worksheet.write(row, 0, 'Notas Mais Dadas', secondary_title_format)
    row += 1
    worksheet.write(row, 0, 'Nota', header_format)
    worksheet.write(row, 1, 'Total', header_format)
    row += 1
    for nota in context['notas_mais_dadas']:
        worksheet.write(row, 0, nota['nota_visita'], data_format)
        worksheet.write(row, 1, nota['total'], data_format)
        row += 1
    row += 1

    # Idades mais visitadas
    worksheet.write(row, 0, 'Idades Mais Visitadas', secondary_title_format)
    row += 1
    worksheet.write(row, 0, 'Idade', header_format)
    worksheet.write(row, 1, 'Total', header_format)
    row += 1
    for idade in context['idades_mais_visitadas']:
        worksheet.write(row, 0, idade['idade'], data_format)
        worksheet.write(row, 1, idade['total'], data_format)
        row += 1

    workbook.close()

    # Retornar o arquivo Excel como uma resposta HTTP para download
    with open('relatorio_promar.xlsx', 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=relatorio_promar.xlsx'

    return response
