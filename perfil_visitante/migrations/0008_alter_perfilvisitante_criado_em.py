# Generated by Django 5.0.6 on 2024-07-04 12:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil_visitante', '0007_perfilvisitante_criado_em'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilvisitante',
            name='criado_em',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
    ]