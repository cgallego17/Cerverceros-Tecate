from django.contrib import admin
from .models import Jugador, Equipo, Partido, Noticia, Boleto, TablaPosiciones


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nombre', 'posicion', 'activo']
    list_filter = ['posicion', 'activo']
    search_fields = ['nombre', 'numero']


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad']
    search_fields = ['nombre', 'ciudad']


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'equipo_local', 'equipo_visitante', 'carreras_local', 'carreras_visitante', 'estado']
    list_filter = ['estado', 'temporada']
    search_fields = ['equipo_local__nombre', 'equipo_visitante__nombre']
    date_hierarchy = 'fecha'


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_publicacion', 'autor', 'destacada']
    list_filter = ['destacada', 'fecha_publicacion']
    search_fields = ['titulo', 'contenido']
    date_hierarchy = 'fecha_publicacion'


@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ['partido', 'tipo', 'precio', 'cantidad_disponible']
    list_filter = ['tipo']
    search_fields = ['partido__equipo_local__nombre', 'partido__equipo_visitante__nombre']


@admin.register(TablaPosiciones)
class TablaPosicionesAdmin(admin.ModelAdmin):
    list_display = ['equipo', 'temporada', 'ganados', 'perdidos', 'porcentaje']
    list_filter = ['temporada']
    search_fields = ['equipo__nombre']
