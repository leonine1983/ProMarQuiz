from django.shortcuts import render, redirect
from .models import PerfilVisitante
from quiz.models import Pergunta, Resposta, VisitantePerguntaResposta
from .forms import PerfilVisitanteForm

def criar_perfil_visitante(request):
    if request.method == 'POST':
        form = PerfilVisitanteForm(request.POST)
        if form.is_valid():
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
        
        return redirect('resultado_quiz')
    
    return render(request, 'responder_perguntas.html', {'perfil_visitante': perfil_visitante, 'perguntas': perguntas, 'respostas': respostas})

def resultado_quiz(request):
    # Implementar lógica para exibir o resultado do quiz, se necessário
    return render(request, 'resultado_quiz.html')
