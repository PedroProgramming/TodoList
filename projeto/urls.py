from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tarefa.urls')),
    path('admin_sistema/', include('admins.urls')),
    path('auth/', include('usuarios.urls')),
    path('captcha/', include('captcha.urls')),
]
