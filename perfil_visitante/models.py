from django.db import models

class PerfilVisitante(models.Model):
    NOTA_VISITA_CHOICES = (
        (1, '01'),
        (2, '02'),
        (3, '03'),
        (4, '04'),
        (5, '05'),
        (6, '06'),
        (7, '07'),
        (8, '08'),
        (9, '09'),
        (10, '10'),
    )

    IDADE_CHOICES = (
        ('5-7', '5, 6 ou 7 anos'),
        ('7-9', '7, 8 ou 9 anos'),
        ('10-12', '10, 11 ou 12 anos'),
        ('mais_de_12', 'Tenho mais que 12 anos'),
    )

    TURMA_CHOICES = (
        ('1', '1º ano do Fundamental'),
        ('2', '2º ano do Fundamental'),
        ('3', '3º ano do Fundamental'),
        ('4', '4º ano do Fundamental'),
        ('5', '5º ano do Fundamental'),
    )

    MUNICIPIO_CHOICES = (
        ('Itaparica', 'Itaparica'),
        ('Vera Cruz', 'Vera Cruz'),
        ('Outro', 'Outro'),
    )

    GOSTOU_CHOICES = (
        ('1', 'SIM'),
        ('0', 'NÃO')
    )
    nome_completo = models.CharField(max_length=100,null=True)     
    nota_visita = models.IntegerField(choices=NOTA_VISITA_CHOICES)
    gostou_visita = models.CharField(max_length=100, choices=GOSTOU_CHOICES) 
    idade = models.CharField(max_length=20, choices=IDADE_CHOICES)
    turma = models.CharField(max_length=50, choices=TURMA_CHOICES)
    municipio_escola = models.CharField(max_length=50, choices=MUNICIPIO_CHOICES)

    class Meta:
        ordering = ['nome_completo']

    def __str__(self):
        return f"Perfil de Visitante {self.id}"
