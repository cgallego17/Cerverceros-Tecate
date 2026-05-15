from django.core.management.base import BaseCommand
from equipo.models import (
    HeroSlide, Producto, CategoriaProducto, ItemFaq,
    SkillProgress, ArticuloNoticia, ImagenInstagram,
    Jugador, Equipo, Partido
)
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Crea contenido de prueba para todas las secciones del inicio'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando contenido de prueba...\n')

        # Hero Slides
        self.stdout.write('- Hero Slides...')
        HeroSlide.objects.all().delete()
        HeroSlide.objects.create(
            subtitulo="BIENVENIDO A CERVECEROS",
            titulo_linea1="PASIÓN POR EL",
            titulo_linea2="BÉISBOL",
            imagen_url="https://placehold.co/1920x800/1a1a1a/e31e24?text=HERO+SLIDE+1+(1920x800)",
            btn1_texto="VER EQUIPO",
            btn1_url="/equipo/",
            btn2_texto="COMPRAR BOLETOS",
            btn2_url="/boleteria/",
            orden=1,
            activo=True
        )
        HeroSlide.objects.create(
            subtitulo="TEMPORADA 2026",
            titulo_linea1="LÍDERES DE LA",
            titulo_linea2="LIGA",
            imagen_url="https://placehold.co/1920x800/2a2a2a/e31e24?text=HERO+SLIDE+2+(1920x800)",
            btn1_texto="VER RESULTADOS",
            btn1_url="/resultados/",
            orden=2,
            activo=True
        )

        # Productos
        self.stdout.write('- Productos de tienda...')
        cat_ropa, _ = CategoriaProducto.objects.get_or_create(nombre="Ropa")
        cat_acc, _ = CategoriaProducto.objects.get_or_create(nombre="Accesorios")
        
        Producto.objects.filter(destacado=True).delete()
        productos = [
            {"nombre": "Jersey Oficial 2026", "precio": 899.00, "precio_anterior": 1299.00, "badge": "sale", "categoria": cat_ropa},
            {"nombre": "Gorra Cerveceros Roja", "precio": 349.00, "badge": "new", "categoria": cat_acc},
            {"nombre": "Playera Conmemorativa", "precio": 499.00, "badge": "", "categoria": cat_ropa},
            {"nombre": "Sudadera con Capucha", "precio": 799.00, "badge": "", "categoria": cat_ropa},
            {"nombre": "Balón Autografiado", "precio": 1499.00, "precio_anterior": 1799.00, "badge": "sale", "categoria": cat_acc},
            {"nombre": "Taza Cerveceros", "precio": 199.00, "badge": "new", "categoria": cat_acc},
            {"nombre": "Chamarra Varsity", "precio": 1299.00, "badge": "", "categoria": cat_ropa},
            {"nombre": "Llavero Logo Equipo", "precio": 99.00, "badge": "new", "categoria": cat_acc},
        ]
        
        for i, prod in enumerate(productos, 1):
            Producto.objects.create(
                nombre=prod["nombre"],
                descripcion=f"Producto oficial de Cerveceros de Tecate. {prod['nombre']}.",
                categoria=prod["categoria"],
                precio=prod["precio"],
                precio_anterior=prod.get("precio_anterior"),
                badge=prod["badge"],
                destacado=True,
                activo=True
            )

        # Skills Progress
        self.stdout.write('- Barras de progreso...')
        SkillProgress.objects.all().delete()
        skills = [
            {"nombre": "Bateo Efectivo", "porcentaje": 85},
            {"nombre": "Defensa en Campo", "porcentaje": 92},
            {"nombre": "Velocidad de Pitcheo", "porcentaje": 78},
            {"nombre": "Trabajo en Equipo", "porcentaje": 95},
        ]
        for i, skill in enumerate(skills, 1):
            SkillProgress.objects.create(
                nombre=skill["nombre"],
                porcentaje=skill["porcentaje"],
                orden=i,
                activo=True
            )

        # Artículos de Noticias (News Grid)
        self.stdout.write('- Artículos de noticias...')
        ArticuloNoticia.objects.filter(destacado_grid=True).delete()
        noticias = [
            {"titulo": "Victoria Épica en Extra Innings", "tipo": "texto", "descripcion": "Los Cerveceros se imponen 8-7 en emocionante partido de 12 entradas."},
            {"titulo": "Nuevo Récord de Asistencia", "tipo": "imagen"},
            {"titulo": "Pitcher del Mes: Miguel Torres", "tipo": "texto", "descripcion": "Nuestro as del pitcheo recibe reconocimiento de la liga."},
            {"titulo": "Día de la Familia Cervecera", "tipo": "imagen"},
            {"titulo": "Racha de 5 Victorias Consecutivas", "tipo": "texto", "descripcion": "El equipo demuestra su poderío ofensivo y defensivo."},
            {"titulo": "Entrenamiento de Pretemporada", "tipo": "imagen"},
            {"titulo": "Firma de Nuevo Jugador Estrella", "tipo": "texto", "descripcion": "Refuerzo de lujo para la temporada 2026."},
            {"titulo": "Noche de Fuegos Artificiales", "tipo": "imagen"},
        ]
        for i, noticia in enumerate(noticias, 1):
            ArticuloNoticia.objects.create(
                titulo=noticia["titulo"],
                descripcion=noticia.get("descripcion", ""),
                tipo=noticia["tipo"],
                destacado_grid=True,
                orden=i,
                activo=True
            )

        # FAQ / Acordeón
        self.stdout.write('- Preguntas frecuentes...')
        ItemFaq.objects.all().delete()
        faqs = [
            {"titulo": "PROJECT PLANNING", "contenido": "Phasellus vitae arcu hendrerit ipsum bibendum aliquet eliante ue habitant morbi tristique senectus."},
            {"titulo": "REFURBISHMENT", "contenido": "Phasellus vitae arcu hendrerit ipsum bibendum aliquet eliante ue habitant morbi tristique senectus."},
            {"titulo": "GENERAL CONTRACTING", "contenido": "Phasellus vitae arcu hendrerit ipsum bibendum aliquet eliante ue habitant morbi tristique senectus."},
            {"titulo": "INTERIOR DESIGN", "contenido": "Phasellus vitae arcu hendrerit ipsum bibendum aliquet eliante ue habitant morbi tristique senectus."},
        ]
        for i, faq in enumerate(faqs, 1):
            ItemFaq.objects.create(
                titulo=faq["titulo"],
                contenido=faq["contenido"],
                orden=i,
                activo=True
            )

        # Jugador destacado
        self.stdout.write('- Jugador destacado...')
        cerveceros, _ = Equipo.objects.get_or_create(
            nombre="Cerveceros de Tecate",
            defaults={"ciudad": "Tecate"}
        )
        
        Jugador.objects.filter(destacado_inicio=True).update(destacado_inicio=False)
        jugador, created = Jugador.objects.get_or_create(
            numero=23,
            defaults={
                "nombre": "Carlos Rodríguez",
                "posicion": "P",
                "biografia": "Carlos es nuestro pitcher estrella con más de 10 años de experiencia en la liga. Ha liderado al equipo a múltiples victorias con su brazo poderoso y precisión excepcional.",
                "altura": "1.88 m",
                "peso": "95 kg",
                "bateo": "Derecha",
                "lanzamiento": "Derecha",
                "activo": True,
                "destacado_inicio": True
            }
        )
        if not created:
            jugador.destacado_inicio = True
            jugador.save()

        # Partidos de ejemplo
        self.stdout.write('- Partidos de ejemplo...')
        equipos_rivales = [
            "Toros de Tijuana",
            "Naranjeros de Hermosillo",
            "Sultanes de Monterrey"
        ]
        
        for nombre_equipo in equipos_rivales:
            Equipo.objects.get_or_create(
                nombre=nombre_equipo,
                defaults={"ciudad": nombre_equipo.split()[-1]}
            )

        self.stdout.write(self.style.SUCCESS('\n✓ Contenido de prueba creado exitosamente!'))
        self.stdout.write(self.style.SUCCESS('Ahora puedes editar todo desde el panel de administración en /admin/'))
