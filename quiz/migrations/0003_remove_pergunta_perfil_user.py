# Generated by Django 5.0.6 on 2024-06-20 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_pergunta_perfil_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pergunta',
            name='perfil_user',
        ),
    ]