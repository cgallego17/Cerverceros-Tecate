from django.urls import path
from . import panel_views

app_name = 'panel'

urlpatterns = [
    # Auth
    path('login/', panel_views.panel_login, name='login'),
    path('logout/', panel_views.panel_logout, name='logout'),
    path('', panel_views.dashboard, name='dashboard'),

    # Hero Slides
    path('hero/', panel_views.hero_lista, name='hero_lista'),
    path('hero/nuevo/', panel_views.hero_form, name='hero_nuevo'),
    path('hero/<int:pk>/editar/', panel_views.hero_form, name='hero_editar'),
    path('hero/<int:pk>/eliminar/', panel_views.hero_eliminar, name='hero_eliminar'),

    # Patrocinadores
    path('patrocinadores/', panel_views.patrocinadores_lista, name='patrocinadores_lista'),
    path('patrocinadores/nuevo/', panel_views.patrocinador_form, name='patrocinador_nuevo'),
    path('patrocinadores/<int:pk>/editar/', panel_views.patrocinador_form, name='patrocinador_editar'),
    path('patrocinadores/<int:pk>/eliminar/', panel_views.patrocinador_eliminar, name='patrocinador_eliminar'),

    # Categorías de Producto
    path('categorias/', panel_views.categorias_lista, name='categorias_lista'),
    path('categorias/nuevo/', panel_views.categoria_form, name='categoria_nueva'),
    path('categorias/<int:pk>/editar/', panel_views.categoria_form, name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', panel_views.categoria_eliminar, name='categoria_eliminar'),

    # Productos
    path('productos/', panel_views.productos_lista, name='productos_lista'),
    path('productos/nuevo/', panel_views.producto_form, name='producto_nuevo'),
    path('productos/<int:pk>/editar/', panel_views.producto_form, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', panel_views.producto_eliminar, name='producto_eliminar'),

    # FAQ
    path('faq/', panel_views.faq_lista, name='faq_lista'),
    path('faq/nuevo/', panel_views.faq_form, name='faq_nueva'),
    path('faq/<int:pk>/editar/', panel_views.faq_form, name='faq_editar'),
    path('faq/<int:pk>/eliminar/', panel_views.faq_eliminar, name='faq_eliminar'),

    # Noticias
    path('noticias/', panel_views.noticias_lista, name='noticias_lista'),
    path('noticias/nuevo/', panel_views.noticia_form, name='noticia_nueva'),
    path('noticias/<int:pk>/editar/', panel_views.noticia_form, name='noticia_editar'),
    path('noticias/<int:pk>/eliminar/', panel_views.noticia_eliminar, name='noticia_eliminar'),

    # Jugadores
    path('jugadores/', panel_views.jugadores_lista, name='jugadores_lista'),
    path('jugadores/nuevo/', panel_views.jugador_form, name='jugador_nuevo'),
    path('jugadores/<int:pk>/editar/', panel_views.jugador_form, name='jugador_editar'),
    path('jugadores/<int:pk>/eliminar/', panel_views.jugador_eliminar, name='jugador_eliminar'),

    # Usuarios
    path('usuarios/', panel_views.usuarios_lista, name='usuarios_lista'),
    path('usuarios/nuevo/', panel_views.usuario_crear, name='usuario_nuevo'),
    path('usuarios/<int:pk>/editar/', panel_views.usuario_editar, name='usuario_editar'),
    path('usuarios/<int:pk>/eliminar/', panel_views.usuario_eliminar, name='usuario_eliminar'),

    # Roles
    path('roles/', panel_views.roles_lista, name='roles_lista'),
    path('roles/nuevo/', panel_views.rol_crear, name='rol_nuevo'),
    path('roles/<int:pk>/editar/', panel_views.rol_editar, name='rol_editar'),
    path('roles/<int:pk>/eliminar/', panel_views.rol_eliminar, name='rol_eliminar'),

    # Caja Registradora
    path('caja/', panel_views.caja_lista, name='caja_lista'),
    path('caja/nueva/', panel_views.transaccion_crear, name='transaccion_nueva'),
    path('caja/<int:pk>/editar/', panel_views.transaccion_editar, name='transaccion_editar'),
    path('caja/<int:pk>/eliminar/', panel_views.transaccion_eliminar, name='transaccion_eliminar'),
    path('caja/api-tipo-cambio/', panel_views.api_tipo_cambio, name='api_tipo_cambio'),

    # Equipos
    path('equipos/', panel_views.equipos_lista, name='equipos_lista'),
    path('equipos/nuevo/', panel_views.equipo_form, name='equipo_nuevo'),
    path('equipos/<int:pk>/editar/', panel_views.equipo_form, name='equipo_editar'),
    path('equipos/<int:pk>/eliminar/', panel_views.equipo_eliminar, name='equipo_eliminar'),

    # Partidos
    path('partidos/', panel_views.partidos_lista, name='partidos_lista'),
    path('partidos/nuevo/', panel_views.partido_form, name='partido_nuevo'),
    path('partidos/<int:pk>/editar/', panel_views.partido_form, name='partido_editar'),
    path('partidos/<int:pk>/eliminar/', panel_views.partido_eliminar, name='partido_eliminar'),

    # Localizaciones - Países
    path('paises/', panel_views.paises_lista, name='paises_lista'),
    path('paises/nuevo/', panel_views.pais_form, name='pais_nuevo'),
    path('paises/<int:pk>/editar/', panel_views.pais_form, name='pais_editar'),
    path('paises/<int:pk>/eliminar/', panel_views.pais_eliminar, name='pais_eliminar'),

    # Localizaciones - Estados
    path('estados/', panel_views.estados_lista, name='estados_lista'),
    path('estados/nuevo/', panel_views.estado_form, name='estado_nuevo'),
    path('estados/<int:pk>/editar/', panel_views.estado_form, name='estado_editar'),
    path('estados/<int:pk>/eliminar/', panel_views.estado_eliminar, name='estado_eliminar'),

    # Localizaciones - Ciudades
    path('ciudades/', panel_views.ciudades_lista, name='ciudades_lista'),
    path('ciudades/nueva/', panel_views.ciudad_form, name='ciudad_nueva'),
    path('ciudades/<int:pk>/editar/', panel_views.ciudad_form, name='ciudad_editar'),
    path('ciudades/<int:pk>/eliminar/', panel_views.ciudad_eliminar, name='ciudad_eliminar'),

    # Próximo Juego Destacado
    path('proximo-juego/', panel_views.proximo_juego_lista, name='proximo_juego_lista'),
    path('proximo-juego/nuevo/', panel_views.proximo_juego_form, name='proximo_juego_nuevo'),
    path('proximo-juego/<int:pk>/editar/', panel_views.proximo_juego_form, name='proximo_juego_editar'),
    path('proximo-juego/<int:pk>/eliminar/', panel_views.proximo_juego_eliminar, name='proximo_juego_eliminar'),

    # Calendario Overlay
    path('calendario-overlay/', panel_views.calendario_overlay_lista, name='calendario_overlay_lista'),
    path('calendario-overlay/nuevo/', panel_views.calendario_overlay_form, name='calendario_overlay_nuevo'),
    path('calendario-overlay/<int:pk>/editar/', panel_views.calendario_overlay_form, name='calendario_overlay_editar'),
    path('calendario-overlay/<int:pk>/eliminar/', panel_views.calendario_overlay_eliminar, name='calendario_overlay_eliminar'),
]
