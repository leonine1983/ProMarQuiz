from django import forms
from .models import Pergunta, Resposta

class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = ['texto_pergunta']

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['pergunta', 'texto_resposta', 'correta']
