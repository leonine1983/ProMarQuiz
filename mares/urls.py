from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('perfil_visitante.urls')),
    path('admin_quiz/', include('quiz.urls'))
]
