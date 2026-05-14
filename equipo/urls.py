from django.urls import path
from . import views

app_name = 'equipo'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('equipo/', views.nuestro_equipo, name='nuestro_equipo'),
    path('jugador/<int:pk>/', views.jugador_detalle, name='jugador_detalle'),
    path('calendario/', views.calendario, name='calendario'),
    path('resultados/', views.resultados, name='resultados'),
    path('tabla/', views.tabla_posiciones, name='tabla_posiciones'),
    path('noticias/', views.noticias, name='noticias'),
    path('noticia/<int:pk>/', views.noticia_detalle, name='noticia_detalle'),
    path('boleteria/', views.boleteria, name='boleteria'),
    path('partido/<int:pk>/boletos/', views.partido_boletos, name='partido_boletos'),
]
