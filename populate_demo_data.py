import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cerveceros_tecate.settings')
django.setup()

from equipo.models import Jugador, Equipo, Partido, Noticia, Boleto, TablaPosiciones

def crear_equipos():
    print("Creando equipos...")
    
    cerveceros, _ = Equipo.objects.get_or_create(
        nombre="Cerveceros de Tecate",
        defaults={'ciudad': 'Tecate, Baja California'}
    )
    
    equipos_rivales = [
        {'nombre': 'Toros de Tijuana', 'ciudad': 'Tijuana'},
        {'nombre': 'Águilas de Mexicali', 'ciudad': 'Mexicali'},
        {'nombre': 'Sultanes de Monterrey', 'ciudad': 'Monterrey'},
        {'nombre': 'Diablos Rojos', 'ciudad': 'Ciudad de México'},
        {'nombre': 'Naranjeros de Hermosillo', 'ciudad': 'Hermosillo'},
    ]
    
    for equipo_data in equipos_rivales:
        Equipo.objects.get_or_create(**equipo_data)
    
    print(f"✓ {Equipo.objects.count()} equipos creados")

def crear_jugadores():
    print("Creando jugadores...")
    
    jugadores_data = [
        {'nombre': 'Carlos Mendoza', 'numero': 7, 'posicion': 'SS', 'altura': '1.85m', 'peso': '85kg', 'bateo': 'Derecha', 'lanzamiento': 'Derecha', 'biografia': 'Veterano shortstop con 10 años de experiencia en ligas profesionales. Conocido por su defensa sólida y liderazgo en el campo.'},
        {'nombre': 'Miguel Ángel Torres', 'numero': 23, 'posicion': 'P', 'altura': '1.90m', 'peso': '95kg', 'bateo': 'Derecha', 'lanzamiento': 'Derecha', 'biografia': 'Pitcher estrella con un promedio de efectividad de 2.85. Su recta alcanza las 95 millas por hora.'},
        {'nombre': 'Roberto "El Gato" Sánchez', 'numero': 15, 'posicion': 'C', 'altura': '1.80m', 'peso': '90kg', 'bateo': 'Derecha', 'lanzamiento': 'Derecha', 'biografia': 'Catcher experimentado con excelente brazo. Ha ganado 3 Guantes de Oro en su carrera.'},
        {'nombre': 'Fernando Ramírez', 'numero': 10, 'posicion': 'CF', 'altura': '1.83m', 'peso': '82kg', 'bateo': 'Izquierda', 'lanzamiento': 'Derecha', 'biografia': 'Jardinero central con velocidad excepcional. Líder en bases robadas de la temporada pasada.'},
        {'nombre': 'José Luis Hernández', 'numero': 44, 'posicion': '1B', 'altura': '1.88m', 'peso': '100kg', 'bateo': 'Izquierda', 'lanzamiento': 'Izquierda', 'biografia': 'Bateador de poder con 25 jonrones la temporada pasada. Jugador All-Star en 2025.'},
        {'nombre': 'Diego Martínez', 'numero': 5, 'posicion': '2B', 'altura': '1.75m', 'peso': '78kg', 'bateo': 'Derecha', 'lanzamiento': 'Derecha', 'biografia': 'Segunda base ágil con excelente visión de juego. Promedio de bateo de .315.'},
        {'nombre': 'Antonio Reyes', 'numero': 33, 'posicion': '3B', 'altura': '1.82m', 'peso': '88kg', 'bateo': 'Derecha', 'lanzamiento': 'Derecha', 'biografia': 'Tercera base con brazo potente. Conocido por sus jugadas defensivas espectaculares.'},
        {'nombre': 'Luis García', 'numero': 21, 'posicion': 'LF', 'altura': '1.78m', 'peso': '80kg', 'bateo': 'Izquierda', 'lanzamiento': 'Izquierda', 'biografia': 'Jardinero izquierdo con gran capacidad de contacto. Rara vez poncha.'},
        {'nombre': 'Pedro Morales', 'numero': 8, 'posicion': 'RF', 'altura': '1.85m', 'peso': '87kg', 'bateo': 'Derecha', 'lanzamiento': 'Derecha', 'biografia': 'Jardinero derecho con brazo cañón. Ha eliminado a 15 corredores esta temporada.'},
        {'nombre': 'Javier López', 'numero': 19, 'posicion': 'P', 'altura': '1.87m', 'peso': '92kg', 'bateo': 'Derecha', 'lanzamiento': 'Izquierda', 'biografia': 'Pitcher zurdo especialista en relevos. Efectividad de 1.95 en situaciones de alta presión.'},
        {'nombre': 'Ricardo Flores', 'numero': 27, 'posicion': 'DH', 'altura': '1.86m', 'peso': '95kg', 'bateo': 'Derecha', 'lanzamiento': 'Derecha', 'biografia': 'Bateador designado con poder a ambos campos. 18 jonrones en lo que va de temporada.'},
        {'nombre': 'Sergio Castillo', 'numero': 12, 'posicion': 'P', 'altura': '1.91m', 'peso': '98kg', 'bateo': 'Derecha', 'lanzamiento': 'Derecha', 'biografia': 'Pitcher cerrador con 20 salvamentos. Su slider es considerado uno de los mejores de la liga.'},
    ]
    
    for jugador_data in jugadores_data:
        Jugador.objects.get_or_create(
            numero=jugador_data['numero'],
            defaults=jugador_data
        )
    
    print(f"✓ {Jugador.objects.count()} jugadores creados")

def crear_partidos():
    print("Creando partidos...")
    
    cerveceros = Equipo.objects.get(nombre="Cerveceros de Tecate")
    rivales = list(Equipo.objects.exclude(nombre="Cerveceros de Tecate"))
    
    hoy = timezone.now()
    
    partidos_pasados = [
        {'dias': -7, 'rival': rivales[0], 'local': 8, 'visitante': 5, 'estado': 'finalizado'},
        {'dias': -5, 'rival': rivales[1], 'local': 6, 'visitante': 7, 'estado': 'finalizado'},
        {'dias': -3, 'rival': rivales[2], 'local': 10, 'visitante': 3, 'estado': 'finalizado'},
        {'dias': -1, 'rival': rivales[3], 'local': 4, 'visitante': 4, 'estado': 'finalizado'},
    ]
    
    for partido_data in partidos_pasados:
        fecha = hoy + timedelta(days=partido_data['dias'])
        Partido.objects.get_or_create(
            fecha=fecha,
            equipo_local=cerveceros,
            equipo_visitante=partido_data['rival'],
            defaults={
                'carreras_local': partido_data['local'],
                'carreras_visitante': partido_data['visitante'],
                'estado': partido_data['estado'],
                'estadio': 'Estadio Cerveceros de Tecate',
                'temporada': '2026'
            }
        )
    
    partidos_futuros = [
        {'dias': 2, 'rival': rivales[4]},
        {'dias': 5, 'rival': rivales[0]},
        {'dias': 8, 'rival': rivales[1]},
        {'dias': 12, 'rival': rivales[2]},
        {'dias': 15, 'rival': rivales[3]},
    ]
    
    for partido_data in partidos_futuros:
        fecha = hoy + timedelta(days=partido_data['dias'])
        partido, created = Partido.objects.get_or_create(
            fecha=fecha,
            equipo_local=cerveceros,
            equipo_visitante=partido_data['rival'],
            defaults={
                'estado': 'programado',
                'estadio': 'Estadio Cerveceros de Tecate',
                'temporada': '2026'
            }
        )
        
        if created:
            tipos_boletos = [
                {'tipo': 'general', 'precio': 150.00, 'cantidad_disponible': 500, 'seccion': 'General'},
                {'tipo': 'preferente', 'precio': 300.00, 'cantidad_disponible': 200, 'seccion': 'Preferente A'},
                {'tipo': 'vip', 'precio': 600.00, 'cantidad_disponible': 50, 'seccion': 'VIP'},
                {'tipo': 'palco', 'precio': 1200.00, 'cantidad_disponible': 20, 'seccion': 'Palco Premium'},
            ]
            
            for boleto_data in tipos_boletos:
                Boleto.objects.create(
                    partido=partido,
                    **boleto_data
                )
    
    print(f"✓ {Partido.objects.count()} partidos creados")

def crear_noticias():
    print("Creando noticias...")
    
    noticias_data = [
        {
            'titulo': '¡Cerveceros de Tecate Gana el Clásico Regional!',
            'contenido': 'En un emocionante partido que mantuvo a los aficionados al borde de sus asientos, los Cerveceros de Tecate se impusieron 8-5 ante los Toros de Tijuana en el clásico regional. Carlos Mendoza brilló con un jonrón de tres carreras en la séptima entrada que selló la victoria.\n\nEl pitcher Miguel Ángel Torres tuvo una actuación sobresaliente, lanzando 7 entradas completas y permitiendo solo 3 carreras. La afición cervecera llenó el estadio con más de 15,000 espectadores que celebraron esta importante victoria.\n\n"Este triunfo es para nuestra afición que siempre nos apoya", declaró el capitán Carlos Mendoza después del partido.',
            'destacada': True,
            'autor': 'Juan Pérez'
        },
        {
            'titulo': 'Miguel Ángel Torres Nombrado Pitcher de la Semana',
            'contenido': 'La Liga Mexicana de Béisbol ha reconocido la excepcional actuación de nuestro pitcher estrella Miguel Ángel Torres, nombrándolo Pitcher de la Semana.\n\nTorres ha mantenido una efectividad de 2.85 en sus últimas tres salidas, con 25 ponches y solo 4 bases por bolas. Su recta alcanza consistentemente las 95 millas por hora, convirtiéndolo en uno de los lanzadores más temidos de la liga.\n\n"Es un honor recibir este reconocimiento, pero el crédito es de todo el equipo", comentó Torres humildemente.',
            'destacada': True,
            'autor': 'María González'
        },
        {
            'titulo': 'Venta Especial de Boletos para el Próximo Partido',
            'contenido': 'Los Cerveceros de Tecate anuncian una promoción especial para el próximo partido del viernes. Los primeros 1000 aficionados recibirán una gorra conmemorativa del equipo.\n\nAdemás, habrá descuentos del 20% en boletos de zona general para familias. No te pierdas esta oportunidad de apoyar a tu equipo favorito.\n\nLos boletos están disponibles en taquilla y en línea. ¡Nos vemos en el estadio!',
            'destacada': False,
            'autor': 'Departamento de Marketing'
        },
        {
            'titulo': 'Roberto Sánchez Alcanza 100 Juegos con Cerveceros',
            'contenido': 'El catcher Roberto "El Gato" Sánchez celebró un hito importante en su carrera al alcanzar 100 juegos con la camiseta de los Cerveceros de Tecate.\n\nSánchez, conocido por su defensa impecable y liderazgo detrás del plato, ha sido fundamental en el éxito del equipo esta temporada. Con 3 Guantes de Oro en su carrera, es considerado uno de los mejores receptores de la liga.\n\n"Jugar para Cerveceros ha sido un sueño hecho realidad. Esta afición es increíble", expresó emocionado Sánchez.',
            'destacada': False,
            'autor': 'Carlos Ruiz'
        },
        {
            'titulo': 'Cerveceros Lidera la Tabla de Posiciones',
            'contenido': 'Con una racha de 5 victorias consecutivas, los Cerveceros de Tecate se colocan en la cima de la tabla de posiciones con un récord de 45-30.\n\nEl equipo ha mostrado un juego consistente tanto en ofensiva como en defensa. Fernando Ramírez lidera la liga en bases robadas con 28, mientras que José Luis Hernández mantiene un impresionante promedio de bateo de .325.\n\nEl manager del equipo declaró: "Estamos jugando nuestro mejor béisbol. El equipo está enfocado en llegar a los playoffs".',
            'destacada': True,
            'autor': 'Luis Martínez'
        },
        {
            'titulo': 'Clínica de Béisbol Juvenil Este Sábado',
            'contenido': 'Los Cerveceros de Tecate invitan a todos los jóvenes aficionados al béisbol a participar en una clínica gratuita este sábado en el estadio.\n\nJugadores profesionales del equipo enseñarán técnicas de bateo, fildeo y pitcheo. La clínica está dirigida a niños y jóvenes de 8 a 16 años.\n\nLas inscripciones son limitadas. Para más información, visita nuestra página web o llama a nuestras oficinas.',
            'destacada': False,
            'autor': 'Departamento de Relaciones Comunitarias'
        }
    ]
    
    for i, noticia_data in enumerate(noticias_data):
        fecha = timezone.now() - timedelta(days=i*2)
        Noticia.objects.get_or_create(
            titulo=noticia_data['titulo'],
            defaults={
                **noticia_data,
                'fecha_publicacion': fecha
            }
        )
    
    print(f"✓ {Noticia.objects.count()} noticias creadas")

def crear_tabla_posiciones():
    print("Creando tabla de posiciones...")
    
    equipos_stats = [
        {'nombre': 'Cerveceros de Tecate', 'jj': 75, 'g': 45, 'p': 30, 'cf': 380, 'cc': 320, 'racha': 'G5'},
        {'nombre': 'Toros de Tijuana', 'jj': 75, 'g': 43, 'p': 32, 'cf': 365, 'cc': 335, 'racha': 'P1'},
        {'nombre': 'Águilas de Mexicali', 'jj': 75, 'g': 41, 'p': 34, 'cf': 355, 'cc': 340, 'racha': 'G2'},
        {'nombre': 'Sultanes de Monterrey', 'jj': 75, 'g': 38, 'p': 37, 'cf': 340, 'cc': 345, 'racha': 'P2'},
        {'nombre': 'Diablos Rojos', 'jj': 75, 'g': 36, 'p': 39, 'cf': 330, 'cc': 360, 'racha': 'G1'},
        {'nombre': 'Naranjeros de Hermosillo', 'jj': 75, 'g': 32, 'p': 43, 'cf': 310, 'cc': 380, 'racha': 'P3'},
    ]
    
    for stats in equipos_stats:
        equipo = Equipo.objects.get(nombre=stats['nombre'])
        TablaPosiciones.objects.get_or_create(
            equipo=equipo,
            temporada='2026',
            defaults={
                'juegos_jugados': stats['jj'],
                'ganados': stats['g'],
                'perdidos': stats['p'],
                'carreras_favor': stats['cf'],
                'carreras_contra': stats['cc'],
                'racha': stats['racha']
            }
        )
    
    print(f"✓ Tabla de posiciones creada")

if __name__ == '__main__':
    print("\n🍺⚾ Poblando base de datos con información demo...\n")
    
    crear_equipos()
    crear_jugadores()
    crear_partidos()
    crear_noticias()
    crear_tabla_posiciones()
    
    print("\n✅ ¡Base de datos poblada exitosamente!")
    print("\nEstadísticas:")
    print(f"  - Equipos: {Equipo.objects.count()}")
    print(f"  - Jugadores: {Jugador.objects.count()}")
    print(f"  - Partidos: {Partido.objects.count()}")
    print(f"  - Noticias: {Noticia.objects.count()}")
    print(f"  - Boletos: {Boleto.objects.count()}")
    print("\n🎉 ¡Listo para usar!")
