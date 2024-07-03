from django.urls import path
from . import views

urlpatterns = [
    path('', views.criar_perfil_visitante, name='criar_perfil_visitante'),
    path('responder/<int:perfil_id>/', views.responder_perguntas, name='responder_perguntas'),
    path('resultado/<int:pk>', views.resultado_quiz, name='resultado_quiz'),
]
