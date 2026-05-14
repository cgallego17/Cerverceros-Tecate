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
]
