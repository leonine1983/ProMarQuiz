from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('perfil_visitante.urls')),
    path('admin_quiz/', include('quiz.urls'))
]
