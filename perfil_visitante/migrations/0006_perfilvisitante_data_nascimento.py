# Generated by Django 5.0.6 on 2024-07-04 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil_visitante', '0005_alter_perfilvisitante_gostou_visita'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilvisitante',
            name='data_nascimento',
            field=models.DateField(null=True),
        ),
    ]
