from django import forms
from .models import Pergunta, Resposta

class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = ['texto_pergunta']

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['texto_resposta', 'correta']

        correta = forms.BooleanField(
            label="Sinalizar que essa é a opção verdadeira"
            
        )
