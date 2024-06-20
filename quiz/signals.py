from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from perfil_visitante.models import PerfilVisitante

@receiver(post_migrate)
def criar_perguntas_e_respostas(sender, **kwargs):
    Pergunta = apps.get_model('quiz', 'Pergunta')
    Resposta = apps.get_model('quiz', 'Resposta')

    if Pergunta.objects.exists():
        return

    perfil_visitante = PerfilVisitante.objects.create(nome='Perfil Padrão', idade='5-7', turma='1', municipio_escola='Itaparica')

    # Criar perguntas
    pergunta1 = Pergunta.objects.create(perfil_user=perfil_visitante, texto_pergunta="Um coral é")
    pergunta2 = Pergunta.objects.create(perfil_user=perfil_visitante, texto_pergunta="O Projeto Mares cuida dos:")
    pergunta3 = Pergunta.objects.create(perfil_user=perfil_visitante, texto_pergunta="Os corais servem como")
    pergunta4 = Pergunta.objects.create(perfil_user=perfil_visitante, texto_pergunta="Como podemos conservar o oceano?")
    pergunta5 = Pergunta.objects.create(perfil_user=perfil_visitante, texto_pergunta="Quem é o inimigo dos corais?")

    # Criar respostas para cada pergunta
    Resposta.objects.create(pergunta=pergunta1, texto_resposta="a-Um animal", correta=True)
    Resposta.objects.create(pergunta=pergunta1, texto_resposta="b-Um ser humano", correta=False)
    Resposta.objects.create(pergunta=pergunta1, texto_resposta="c-Um brinquedo", correta=False)

    Resposta.objects.create(pergunta=pergunta2, texto_resposta="a-Corais", correta=True)
    Resposta.objects.create(pergunta=pergunta2, texto_resposta="b-Carros", correta=False)
    Resposta.objects.create(pergunta=pergunta2, texto_resposta="c-Celulares", correta=False)

    Resposta.objects.create(pergunta=pergunta3, texto_resposta="a-Pedras", correta=False)
    Resposta.objects.create(pergunta=pergunta3, texto_resposta="b-Casa para os peixes", correta=True)
    Resposta.objects.create(pergunta=pergunta3, texto_resposta="c-Brinquedo para crianças", correta=False)

    Resposta.objects.create(pergunta=pergunta4, texto_resposta="a-Não jogando lixo nele", correta=True)
    Resposta.objects.create(pergunta=pergunta4, texto_resposta="b-Brincando na praia", correta=False)
    Resposta.objects.create(pergunta=pergunta4, texto_resposta="c-Olhando os peixes", correta=False)

    Resposta.objects.create(pergunta=pergunta5, texto_resposta="a-a chuva", correta=False)
    Resposta.objects.create(pergunta=pergunta5, texto_resposta="b-o vento", correta=False)
    Resposta.objects.create(pergunta=pergunta5, texto_resposta="c-o lixo", correta=True)
