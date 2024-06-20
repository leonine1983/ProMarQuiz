from django import forms
from .models import PerfilVisitante

class PerfilVisitanteForm(forms.ModelForm):
    class Meta:
        model = PerfilVisitante
        fields = ['nome_completo','nota_visita', 'gostou_visita', 'idade', 'turma', 'municipio_escola']
