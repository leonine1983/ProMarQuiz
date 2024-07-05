from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.relatorio_completo, name='relatorio'),
    path('pergunta/criar/', views.criar_pergunta, name='criar_pergunta'),
    path('pergunta/editar/<int:pergunta_id>/', views.editar_pergunta, name='editar_pergunta'),
    path('resposta/criar/<int:pergunta_id>', views.criar_resposta, name='criar_resposta'),
    path('resposta/editar/<int:resposta_id>/', views.editar_resposta, name='editar_resposta'),
]
