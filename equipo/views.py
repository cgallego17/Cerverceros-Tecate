from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import (
    Jugador, Partido, Noticia, Boleto, TablaPosiciones,
    HeroSlide, Patrocinador, Producto, CategoriaProducto, ItemFaq,
    SkillProgress, ArticuloNoticia, ImagenInstagram,
)


def inicio(request):
    # Hero
    hero_slides = HeroSlide.objects.filter(activo=True).order_by('orden')
    patrocinadores = Patrocinador.objects.filter(activo=True).order_by('orden')

    # Partidos
    proximos_partidos = Partido.objects.filter(
        fecha__gte=timezone.now(), estado='programado'
    ).order_by('fecha')[:3]
    proximo_partido = proximos_partidos.first()

    # Jugador destacado
    jugador_destacado = Jugador.objects.filter(activo=True, destacado_inicio=True).first()

    # Noticias para la grilla del home (8 más recientes con imagen)
    noticias_inicio = Noticia.objects.all().order_by('-fecha_publicacion')[:8]
    noticias_destacadas = Noticia.objects.filter(destacada=True)[:3]

    # Productos destacados en el carrusel de tienda
    productos_destacados = Producto.objects.filter(activo=True, destacado=True).order_by('nombre')

    # FAQ / Acordeón
    faq_items = ItemFaq.objects.filter(activo=True).order_by('orden')

    # Skills Progress
    skills = SkillProgress.objects.filter(activo=True).order_by('orden')

    # Artículos de Noticias (News Grid) - Usando noticias del panel
    articulos_news = Noticia.objects.filter(activo=True).order_by('-fecha_publicacion')[:6]

    # Imágenes de Instagram
    imagenes_instagram = ImagenInstagram.objects.filter(activo=True).order_by('orden')[:4]

    context = {
        'hero_slides': hero_slides,
        'patrocinadores': patrocinadores,
        'proximos_partidos': proximos_partidos,
        'proximo_partido': proximo_partido,
        'jugador_destacado': jugador_destacado,
        'noticias_inicio': noticias_inicio,
        'noticias_destacadas': noticias_destacadas,
        'productos_destacados': productos_destacados,
        'faq_items': faq_items,
        'skills': skills,
        'articulos_news': articulos_news,
        'imagenes_instagram': imagenes_instagram,
    }
    return render(request, 'equipo/inicio.html', context)


def tienda(request):
    categorias = CategoriaProducto.objects.all()
    categoria_slug = request.GET.get('categoria')
    productos = Producto.objects.filter(activo=True)
    categoria_activa = None
    if categoria_slug:
        categoria_activa = get_object_or_404(CategoriaProducto, slug=categoria_slug)
        productos = productos.filter(categoria=categoria_activa)
    productos = productos.order_by('nombre')
    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_activa': categoria_activa,
        'total_productos': Producto.objects.filter(activo=True).count(),
    }
    return render(request, 'equipo/tienda.html', context)


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    relacionados = Producto.objects.filter(
        activo=True, categoria=producto.categoria
    ).exclude(pk=pk)[:4]
    context = {
        'producto': producto,
        'relacionados': relacionados,
    }
    return render(request, 'equipo/producto_detalle.html', context)


def nuestro_equipo(request):
    jugadores = Jugador.objects.filter(activo=True)
    context = {
        'jugadores': jugadores,
    }
    return render(request, 'equipo/nuestro_equipo.html', context)


def jugador_detalle(request, pk):
    jugador = get_object_or_404(Jugador, pk=pk)
    context = {
        'jugador': jugador,
    }
    return render(request, 'equipo/jugador_detalle.html', context)


def calendario(request):
    partidos_futuros = Partido.objects.filter(
        fecha__gte=timezone.now()
    ).order_by('fecha')
    partidos_pasados = Partido.objects.filter(
        fecha__lt=timezone.now()
    ).order_by('-fecha')
    
    context = {
        'partidos_futuros': partidos_futuros,
        'partidos_pasados': partidos_pasados,
    }
    return render(request, 'equipo/calendario.html', context)


def resultados(request):
    partidos_finalizados = Partido.objects.filter(
        estado='finalizado'
    ).order_by('-fecha')
    
    context = {
        'partidos': partidos_finalizados,
    }
    return render(request, 'equipo/resultados.html', context)


def tabla_posiciones(request):
    tabla = TablaPosiciones.objects.all()
    
    context = {
        'tabla': tabla,
    }
    return render(request, 'equipo/tabla_posiciones.html', context)


def noticias(request):
    todas_noticias = Noticia.objects.all()
    
    context = {
        'noticias': todas_noticias,
    }
    return render(request, 'equipo/noticias.html', context)


def noticia_detalle(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    context = {
        'noticia': noticia,
    }
    return render(request, 'equipo/noticia_detalle.html', context)


def boleteria(request):
    partidos_disponibles = Partido.objects.filter(
        fecha__gte=timezone.now(),
        estado='programado'
    ).order_by('fecha')
    
    context = {
        'partidos': partidos_disponibles,
    }
    return render(request, 'equipo/boleteria.html', context)


def partido_boletos(request, pk):
    partido = get_object_or_404(Partido, pk=pk)
    boletos = Boleto.objects.filter(partido=partido, cantidad_disponible__gt=0)
    
    context = {
        'partido': partido,
        'boletos': boletos,
    }
    return render(request, 'equipo/partido_boletos.html', context)
