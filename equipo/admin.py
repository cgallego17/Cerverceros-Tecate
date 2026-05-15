from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Jugador, Equipo, Partido, Noticia, Boleto, TablaPosiciones,
    HeroSlide, Patrocinador, Producto, CategoriaProducto, ItemFaq,
    SkillProgress, ArticuloNoticia, ImagenInstagram,
)

# ── Personalización del panel ──────────────────────────────────────────────────
admin.site.site_header = "Cerveceros de Tecate"
admin.site.site_title = "Panel Administrativo"
admin.site.index_title = "Administración del Sitio"


# ── Equipo / Jugadores ─────────────────────────────────────────────────────────

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nombre', 'posicion', 'preview_foto', 'activo', 'destacado_inicio']
    list_editable = ['activo', 'destacado_inicio']
    list_filter = ['posicion', 'activo', 'destacado_inicio']
    search_fields = ['nombre', 'numero']
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'numero', 'posicion', 'foto')
        }),
        ('Estadísticas', {
            'fields': ('altura', 'peso', 'bateo', 'lanzamiento', 'fecha_nacimiento')
        }),
        ('Biografía', {
            'fields': ('biografia',)
        }),
        ('Configuración', {
            'fields': ('activo', 'destacado_inicio'),
        }),
    )

    @admin.display(description='Foto')
    def preview_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;">', obj.foto.url)
        return '—'


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'preview_logo']
    search_fields = ['nombre', 'ciudad']
    fieldsets = (
        ('Información del Equipo', {
            'fields': ('nombre', 'ciudad', 'logo')
        }),
    )

    @admin.display(description='Logo')
    def preview_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.logo.url)
        return '—'


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'equipo_local', 'equipo_visitante', 'carreras_local', 'carreras_visitante', 'estado']
    list_editable = ['estado']
    list_filter = ['estado', 'temporada']
    search_fields = ['equipo_local__nombre', 'equipo_visitante__nombre']
    date_hierarchy = 'fecha'


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'preview_imagen', 'fecha_publicacion', 'autor', 'destacada']
    list_editable = ['destacada']
    list_filter = ['destacada', 'fecha_publicacion']
    search_fields = ['titulo', 'contenido']
    date_hierarchy = 'fecha_publicacion'
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'contenido', 'imagen')
        }),
        ('Información', {
            'fields': ('autor', 'fecha_publicacion', 'destacada')
        }),
    )

    @admin.display(description='Imagen')
    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.imagen.url)
        return '—'


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


# ── Home – Hero Slider ─────────────────────────────────────────────────────────

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['orden', 'titulo_linea1', 'titulo_linea2', 'preview_imagen', 'activo']
    list_editable = ['orden', 'activo']
    list_display_links = ['titulo_linea1']
    ordering = ['orden']
    fieldsets = (
        ('Contenido', {
            'fields': ('subtitulo', 'titulo_linea1', 'titulo_linea2')
        }),
        ('Imagen de fondo', {
            'fields': ('imagen', 'imagen_url'),
            'description': 'Sube una imagen o proporciona una URL externa.'
        }),
        ('Botones', {
            'fields': (('btn1_texto', 'btn1_url'), ('btn2_texto', 'btn2_url')),
            'classes': ('collapse',),
        }),
        ('Configuración', {
            'fields': ('orden', 'activo'),
        }),
    )

    @admin.display(description='Vista previa')
    def preview_imagen(self, obj):
        url = obj.imagen_bg
        if url:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', url)
        return '—'


# ── Home – Patrocinadores ──────────────────────────────────────────────────────

@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
    list_display = ['orden', 'nombre', 'preview_logo', 'activo']
    list_editable = ['orden', 'activo']
    list_display_links = ['nombre']
    ordering = ['orden']

    @admin.display(description='Logo')
    def preview_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:36px;">', obj.logo.url)
        return '—'


# ── Módulo de Productos ────────────────────────────────────────────────────────

@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'preview_imagen', 'nombre', 'categoria',
        'precio', 'precio_anterior', 'badge', 'destacado', 'activo',
    ]
    list_editable = ['precio', 'precio_anterior', 'badge', 'destacado', 'activo']
    list_display_links = ['nombre']
    list_filter = ['categoria', 'badge', 'activo', 'destacado']
    search_fields = ['nombre', 'descripcion']
    fieldsets = (
        ('Información del producto', {
            'fields': ('nombre', 'descripcion', 'categoria', 'imagen')
        }),
        ('Precio', {
            'fields': (('precio', 'precio_anterior'), 'badge'),
        }),
        ('Visibilidad', {
            'fields': ('activo', 'destacado'),
        }),
    )

    @admin.display(description='Imagen')
    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="height:48px;border-radius:4px;">', obj.imagen.url)
        return '—'


# ── Home – FAQ / Acordeón ──────────────────────────────────────────────────────

@admin.register(ItemFaq)
class ItemFaqAdmin(admin.ModelAdmin):
    list_display = ['orden', 'titulo', 'activo']
    list_editable = ['orden', 'activo']
    list_display_links = ['titulo']
    ordering = ['orden']


# ── Home – Skills Progress ─────────────────────────────────────────────────────

@admin.register(SkillProgress)
class SkillProgressAdmin(admin.ModelAdmin):
    list_display = ['orden', 'nombre', 'porcentaje', 'activo']
    list_editable = ['orden', 'porcentaje', 'activo']
    list_display_links = ['nombre']
    ordering = ['orden']


# ── Home – News Grid ───────────────────────────────────────────────────────────

@admin.register(ArticuloNoticia)
class ArticuloNoticiaAdmin(admin.ModelAdmin):
    list_display = ['orden', 'titulo', 'tipo', 'preview_imagen', 'destacado_grid', 'activo']
    list_editable = ['orden', 'tipo', 'destacado_grid', 'activo']
    list_display_links = ['titulo']
    list_filter = ['tipo', 'destacado_grid', 'activo']
    search_fields = ['titulo', 'descripcion']
    ordering = ['orden']
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'descripcion', 'tipo', 'imagen', 'enlace')
        }),
        ('Configuración', {
            'fields': ('orden', 'destacado_grid', 'activo')
        }),
    )

    @admin.display(description='Imagen')
    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.imagen.url)
        return '—'


# ── Home – Instagram Gallery ───────────────────────────────────────────────────

@admin.register(ImagenInstagram)
class ImagenInstagramAdmin(admin.ModelAdmin):
    list_display = ['orden', 'preview_imagen', 'activo']
    list_editable = ['activo']
    list_display_links = ['orden', 'preview_imagen']
    ordering = ['orden']
    fieldsets = (
        ('Imagen', {
            'fields': ('imagen', 'imagen_url'),
            'description': 'Sube una imagen o proporciona una URL externa.'
        }),
        ('Configuración', {
            'fields': ('enlace', 'orden', 'activo')
        }),
    )

    @admin.display(description='Vista previa')
    def preview_imagen(self, obj):
        src = obj.imagen_src
        if src:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;">', src)
        return '—'

