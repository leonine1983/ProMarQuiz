# Generated by Django 5.0.6 on 2024-06-20 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_remove_pergunta_perfil_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pergunta',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='resposta',
            options={'ordering': ['pergunta__id', 'texto_resposta']},
        ),
        migrations.CreateModel(
            name='VisitantePerguntaResposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Peguntas_related', to='quiz.pergunta')),
                ('resposta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Respostas_related', to='quiz.resposta')),
            ],
        ),
    ]
