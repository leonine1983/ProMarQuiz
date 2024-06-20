# Generated by Django 5.0.6 on 2024-06-20 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil_visitante', '0003_alter_perfilvisitante_options'),
        ('quiz', '0004_alter_pergunta_options_alter_resposta_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitanteperguntaresposta',
            name='visitante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Visitante_related', to='perfil_visitante.perfilvisitante'),
        ),
    ]