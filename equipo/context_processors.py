from django.utils import timezone

from .models import Partido


def footer_fixtures(request):
    proximos = (
        Partido.objects.filter(fecha__gte=timezone.now(), estado='programado')
        .select_related('equipo_local', 'equipo_visitante')
        .order_by('fecha')[:3]
    )

    fixtures = []
    for partido in proximos:
        local_nombre = (partido.equipo_local.nombre or '').strip()
        visitante_nombre = (partido.equipo_visitante.nombre or '').strip()

        local_is_cerveceros = 'cerveceros' in local_nombre.lower()
        visitante_is_cerveceros = 'cerveceros' in visitante_nombre.lower()

        if local_is_cerveceros and not visitante_is_cerveceros:
            is_home = True
            opponent = visitante_nombre
        elif visitante_is_cerveceros and not local_is_cerveceros:
            is_home = False
            opponent = local_nombre
        else:
            is_home = True
            opponent = visitante_nombre

        fixtures.append(
            {
                'fecha': partido.fecha,
                'is_home': is_home,
                'opponent': opponent,
                'estadio': (partido.estadio or '').strip(),
            }
        )

    return {
        'footer_proximos_partidos': fixtures,
    }
