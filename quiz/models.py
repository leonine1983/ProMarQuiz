from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from perfil_visitante.models import PerfilVisitante

class Pergunta(models.Model):
    texto_pergunta = models.TextField()

      
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.texto_pergunta
  
    
    @receiver(post_migrate)
    def cria_perguntas(sender, **kwargs):
        if not Pergunta.objects.exists():
            pergunta1 = Pergunta.objects.create(texto_pergunta="Um coral é")
            pergunta2 = Pergunta.objects.create(texto_pergunta="O Projeto Mares cuida dos:")
            pergunta3 = Pergunta.objects.create(texto_pergunta="Os corais servem como")
            pergunta4 = Pergunta.objects.create(texto_pergunta="Como podemos conservar o oceano?")
            pergunta5 = Pergunta.objects.create( texto_pergunta="Quem é o inimigo dos corais?")


class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, related_name='respostas', on_delete=models.CASCADE)
    texto_resposta = models.CharField(max_length=100)
    correta = models.BooleanField(default=False)

    class Meta:
        ordering = ['pergunta__id', 'texto_resposta']

    def __str__(self):
        return f'{self.pergunta.texto_pergunta}: {self.texto_resposta}'
    
    @receiver(post_migrate)
    def cria_respostas(sender, **kwargs):
        if not Resposta.objects.exists():
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=1), texto_resposta="a-Um animal", correta=True)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=1), texto_resposta="b-Um ser humano", correta=False)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=1), texto_resposta="c-Um brinquedo", correta=False)

            Resposta.objects.create(pergunta=Pergunta.objects.get(id=2), texto_resposta="a-Corais", correta=True)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=2), texto_resposta="b-Carros", correta=False)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=2), texto_resposta="c-Celulares", correta=False)

            Resposta.objects.create(pergunta=Pergunta.objects.get(id=3), texto_resposta="a-Pedras", correta=False)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=3), texto_resposta="b-Casa para os peixes", correta=True)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=3), texto_resposta="c-Brinquedo para crianças", correta=False)

            Resposta.objects.create(pergunta=Pergunta.objects.get(id=4), texto_resposta="a-Não jogando lixo nele", correta=True)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=4), texto_resposta="b-Brincando na praia", correta=False)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=4), texto_resposta="c-Olhando os peixes", correta=False)

            Resposta.objects.create(pergunta=Pergunta.objects.get(id=5), texto_resposta="a-a chuva", correta=False)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=5), texto_resposta="b-o vento", correta=False)
            Resposta.objects.create(pergunta=Pergunta.objects.get(id=5), texto_resposta="c-o lixo", correta=True)

    
class VisitantePerguntaResposta(models.Model):
    visitante = models.ForeignKey(PerfilVisitante, related_name='Visitante_related', null=True, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, related_name='Peguntas_related', on_delete=models.CASCADE)
    resposta = models.ForeignKey(Resposta, related_name='Respostas_related', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.pergunta.texto_pergunta}: {self.resposta.texto_resposta}'

