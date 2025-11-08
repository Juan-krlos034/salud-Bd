from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# si más adelante agregas otras apps, las puedes incluir igual
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),  # 👈 aquí se conecta tu app usuarios
    path('api/', include('citas.urls')),
]

