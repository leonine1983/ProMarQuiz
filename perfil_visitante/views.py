from django.shortcuts import render, redirect
from quiz.models import Pergunta, Resposta, VisitantePerguntaResposta
from django.contrib import messages

from django.utils import timezone
from datetime import timedelta
from .forms import PerfilVisitanteForm
from .models import PerfilVisitante
import qrcode
from django.conf import settings
import os
import base64
from io import BytesIO


def criar_perfil_visitante(request):
    if request.method == 'POST':
        form = PerfilVisitanteForm(request.POST)
        if form.is_valid():
            nome_completo = form.cleaned_data['nome_completo']
            data_nascimento = form.cleaned_data['data_nascimento']
            
            # Obtém o datetime atual
            agora = timezone.now()
            
            # Calcula o tempo que passou desde o último registro
            ultimo_registro = PerfilVisitante.objects.filter(
                nome_completo=nome_completo,
                data_nascimento=data_nascimento
            ).order_by('-criado_em').first()

            if ultimo_registro:
                tempo_passado = agora - ultimo_registro.criado_em
                
                # Verificar se o tempo passado é menor que uma hora
                if tempo_passado < timedelta(hours=1):
                    # Redirecionar para uma página de aviso
                    messages = f'{(nome_completo).upper()} Aguarde {tempo_passado} para poder preencher novamente o Quiz'
                    return render(request, 'criar_perfil_visitante.html', {'form': form, 'tempo_passado': tempo_passado, 'messages': messages})

            # Se já passou uma hora desde o último registro ou não há registros anteriores, salvar o perfil
            perfil_visitante = form.save()
            return redirect('responder_perguntas', perfil_id=perfil_visitante.id)
    else:
        form = PerfilVisitanteForm()
    
    return render(request, 'criar_perfil_visitante.html', {'form': form})


def responder_perguntas(request, perfil_id):
    perfil_visitante = PerfilVisitante.objects.get(id=perfil_id)
    perguntas = Pergunta.objects.all()
    respostas = Resposta.objects.filter(pergunta__in=perguntas)
    
    if request.method == 'POST':
        for pergunta in perguntas:
            resposta_id = request.POST.get(f'resposta_{pergunta.id}')
            if resposta_id:
                resposta = Resposta.objects.get(id=resposta_id)
                VisitantePerguntaResposta.objects.create(visitante=perfil_visitante, pergunta=pergunta, resposta=resposta)
        
        return redirect('resultado_quiz', pk = perfil_visitante.id )
    
    return render(request, 'responder_perguntas.html', {'perfil_visitante': perfil_visitante, 'perguntas': perguntas, 'respostas': respostas})

def resultado_quiz(request, pk):
    visitante = VisitantePerguntaResposta.objects.filter(visitante = pk)
    visitante_acertos = visitante.filter(resposta__correta = True)
    
    return render(request, 'resultado_quiz.html', {'visitante':visitante, 'acertos': visitante_acertos})


def qr_code(request):
    server_ip = '34.72.23.133'
    
    # Cria o objeto QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Adiciona os dados (neste caso, o endereço IP) ao QR Code
    qr.add_data(f'http://{server_ip}')
    qr.make(fit=True)
    
    # Cria um buffer de memória para salvar a imagem do QR Code
    qr_img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    
    # Converte a imagem para base64
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # URL do arquivo de mídia para ser usado no template
    qr_code_url = f"data:image/png;base64,{qr_code_base64}"
    
    # Contexto para passar para o template
    context = {
        'server_ip': server_ip,
        'qr_code_url': qr_code_url,
    }
    
    return render(request, 'qr_code.html', context)

