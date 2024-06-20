from django.contrib import admin
from quiz.models import *

admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(VisitantePerguntaResposta)