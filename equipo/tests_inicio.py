"""
Tests para la vista de inicio y sus componentes
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import (
    HeroSlide, Patrocinador, Partido, Equipo, Jugador, Noticia,
    Producto, CategoriaProducto, ItemFaq, SkillProgress, ImagenInstagram,
    Ciudad, Estado, Pais
)


class InicioViewTestCase(TestCase):
    """Tests para la vista de inicio"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = Client()
        self.url = reverse('equipo:inicio')
        
        # Crear datos de localización
        self.pais = Pais.objects.create(nombre='México', codigo='MX', activo=True)
        self.estado = Estado.objects.create(nombre='Baja California', pais=self.pais, activo=True)
        self.ciudad = Ciudad.objects.create(nombre='Tecate', estado=self.estado, activo=True)
        
        # Crear equipos
        self.equipo_local = Equipo.objects.create(
            nombre='Cerveceros de Tecate',
            ciudad=self.ciudad
        )
        self.equipo_visitante = Equipo.objects.create(
            nombre='Toros de Tijuana',
            ciudad=self.ciudad
        )
    
    def test_inicio_view_status_code(self):
        """Verificar que la vista de inicio carga correctamente"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_inicio_view_template(self):
        """Verificar que usa el template correcto"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'equipo/inicio.html')
        self.assertTemplateUsed(response, 'equipo/base.html')
    
    def test_inicio_context_hero_slides(self):
        """Verificar que el contexto incluye hero slides"""
        # Crear hero slide
        hero = HeroSlide.objects.create(
            titulo_linea1='Bienvenidos',
            subtitulo='Temporada 2026',
            activo=True,
            orden=1
        )
        
        response = self.client.get(self.url)
        self.assertIn('hero_slides', response.context)
        self.assertEqual(response.context['hero_slides'].count(), 1)
    
    def test_inicio_context_patrocinadores(self):
        """Verificar que el contexto incluye patrocinadores"""
        # Crear patrocinador
        patrocinador = Patrocinador.objects.create(
            nombre='Patrocinador Test',
            activo=True,
            orden=1
        )
        
        response = self.client.get(self.url)
        self.assertIn('patrocinadores', response.context)
        self.assertEqual(response.context['patrocinadores'].count(), 1)
    
    def test_inicio_context_proximos_partidos(self):
        """Verificar que el contexto incluye próximos partidos"""
        # Crear partido futuro
        fecha_futura = timezone.now() + timedelta(days=7)
        partido = Partido.objects.create(
            fecha=fecha_futura,
            equipo_local=self.equipo_local,
            equipo_visitante=self.equipo_visitante,
            estado='programado',
            estadio='Estadio Cerveceros',
            temporada='2026'
        )
        
        response = self.client.get(self.url)
        self.assertIn('proximos_partidos', response.context)
        self.assertIn('proximo_partido', response.context)
        self.assertEqual(response.context['proximos_partidos'].count(), 1)
        self.assertEqual(response.context['proximo_partido'], partido)
    
    def test_inicio_context_jugador_destacado(self):
        """Verificar que el contexto incluye jugador destacado"""
        # Crear jugador destacado
        jugador = Jugador.objects.create(
            nombre='Juan Pérez',
            numero=10,
            posicion='lanzador',
            activo=True,
            destacado_inicio=True
        )
        
        response = self.client.get(self.url)
        self.assertIn('jugador_destacado', response.context)
        self.assertEqual(response.context['jugador_destacado'], jugador)
    
    def test_inicio_context_noticias(self):
        """Verificar que el contexto incluye noticias"""
        # Crear noticias
        noticia1 = Noticia.objects.create(
            titulo='Noticia 1',
            contenido='Contenido de prueba',
            activo=True,
            destacada=True
        )
        noticia2 = Noticia.objects.create(
            titulo='Noticia 2',
            contenido='Contenido de prueba 2',
            activo=True
        )
        
        response = self.client.get(self.url)
        self.assertIn('noticias_inicio', response.context)
        self.assertIn('noticias_destacadas', response.context)
        self.assertIn('articulos_news', response.context)
        
        # Verificar que las noticias activas aparecen
        self.assertTrue(response.context['noticias_inicio'].count() > 0)
        self.assertEqual(response.context['noticias_destacadas'].count(), 1)
    
    def test_inicio_context_productos(self):
        """Verificar que el contexto incluye productos destacados"""
        # Crear categoría y producto
        categoria = CategoriaProducto.objects.create(
            nombre='Ropa'
        )
        producto = Producto.objects.create(
            nombre='Gorra Cerveceros',
            precio=299.00,
            categoria=categoria,
            activo=True,
            destacado=True
        )
        
        response = self.client.get(self.url)
        self.assertIn('productos_destacados', response.context)
        self.assertEqual(response.context['productos_destacados'].count(), 1)
    
    def test_inicio_context_faq(self):
        """Verificar que el contexto incluye items FAQ"""
        # Crear item FAQ
        faq = ItemFaq.objects.create(
            titulo='¿Cómo comprar boletos?',
            contenido='Puedes comprar en línea o en taquilla',
            activo=True,
            orden=1
        )
        
        response = self.client.get(self.url)
        self.assertIn('faq_items', response.context)
        self.assertEqual(response.context['faq_items'].count(), 1)
    
    def test_inicio_context_skills(self):
        """Verificar que el contexto incluye skills progress"""
        # Crear skill
        skill = SkillProgress.objects.create(
            nombre='Bateo',
            porcentaje=85,
            activo=True,
            orden=1
        )
        
        response = self.client.get(self.url)
        self.assertIn('skills', response.context)
        self.assertEqual(response.context['skills'].count(), 1)
    
    def test_inicio_context_instagram(self):
        """Verificar que el contexto incluye imágenes de Instagram"""
        # Crear imagen de Instagram
        instagram = ImagenInstagram.objects.create(
            imagen_url='https://example.com/image.jpg',
            activo=True,
            orden=1
        )
        
        response = self.client.get(self.url)
        self.assertIn('imagenes_instagram', response.context)
        self.assertEqual(response.context['imagenes_instagram'].count(), 1)
    
    def test_inicio_sin_datos(self):
        """Verificar que la vista funciona sin datos"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que las variables de contexto existen aunque estén vacías
        self.assertIn('hero_slides', response.context)
        self.assertIn('patrocinadores', response.context)
        self.assertIn('proximos_partidos', response.context)
        self.assertIn('noticias_inicio', response.context)
        self.assertIn('productos_destacados', response.context)
    
    def test_inicio_noticias_solo_activas(self):
        """Verificar que solo se muestran noticias activas"""
        # Crear noticia activa e inactiva
        noticia_activa = Noticia.objects.create(
            titulo='Noticia Activa',
            contenido='Contenido',
            activo=True
        )
        noticia_inactiva = Noticia.objects.create(
            titulo='Noticia Inactiva',
            contenido='Contenido',
            activo=False
        )
        
        response = self.client.get(self.url)
        articulos = response.context['articulos_news']
        
        # Verificar que solo aparece la noticia activa
        self.assertIn(noticia_activa, articulos)
        self.assertNotIn(noticia_inactiva, articulos)
    
    def test_inicio_partidos_solo_futuros(self):
        """Verificar que solo se muestran partidos futuros"""
        # Crear partido pasado y futuro
        fecha_pasada = timezone.now() - timedelta(days=7)
        fecha_futura = timezone.now() + timedelta(days=7)
        
        partido_pasado = Partido.objects.create(
            fecha=fecha_pasada,
            equipo_local=self.equipo_local,
            equipo_visitante=self.equipo_visitante,
            estado='finalizado',
            estadio='Estadio',
            temporada='2026'
        )
        
        partido_futuro = Partido.objects.create(
            fecha=fecha_futura,
            equipo_local=self.equipo_local,
            equipo_visitante=self.equipo_visitante,
            estado='programado',
            estadio='Estadio',
            temporada='2026'
        )
        
        response = self.client.get(self.url)
        proximos = response.context['proximos_partidos']
        
        # Verificar que solo aparece el partido futuro
        self.assertIn(partido_futuro, proximos)
        self.assertNotIn(partido_pasado, proximos)
    
    def test_inicio_slug_autogenerado(self):
        """Verificar que el slug se genera automáticamente para noticias"""
        noticia = Noticia.objects.create(
            titulo='Noticia de Prueba',
            contenido='Contenido',
            activo=True
        )
        
        # Verificar que el slug se generó
        self.assertIsNotNone(noticia.slug)
        self.assertEqual(noticia.slug, 'noticia-de-prueba')


class NoticiaModelTestCase(TestCase):
    """Tests específicos para el modelo Noticia"""
    
    def test_noticia_slug_generation(self):
        """Verificar generación automática de slug"""
        noticia = Noticia.objects.create(
            titulo='Mi Primera Noticia',
            contenido='Contenido de prueba'
        )
        
        self.assertEqual(noticia.slug, 'mi-primera-noticia')
    
    def test_noticia_defaults(self):
        """Verificar valores por defecto"""
        noticia = Noticia.objects.create(
            titulo='Noticia Test',
            contenido='Contenido'
        )
        
        self.assertTrue(noticia.activo)
        self.assertFalse(noticia.destacada)
        self.assertIsNotNone(noticia.fecha_publicacion)
    
    def test_noticia_str(self):
        """Verificar método __str__"""
        noticia = Noticia.objects.create(
            titulo='Noticia Test',
            contenido='Contenido'
        )
        
        self.assertEqual(str(noticia), 'Noticia Test')
