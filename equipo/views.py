from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Jugador, Partido, Noticia, Boleto, TablaPosiciones


def inicio(request):
    noticias_destacadas = Noticia.objects.filter(destacada=True)[:3]
    proximos_partidos = Partido.objects.filter(
        fecha__gte=timezone.now(),
        estado='programado'
    ).order_by('fecha')[:3]
    ultimos_resultados = Partido.objects.filter(
        estado='finalizado'
    ).order_by('-fecha')[:3]
    
    context = {
        'noticias_destacadas': noticias_destacadas,
        'proximos_partidos': proximos_partidos,
        'ultimos_resultados': ultimos_resultados,
    }
    return render(request, 'equipo/inicio.html', context)


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
