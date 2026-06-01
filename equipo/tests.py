from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Jugador, Partido, Equipo, Noticia, Ciudad, Estado, Pais


class WebsiteViewsTestCase(TestCase):
    """Tests completos para todas las vistas del website"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = Client()
        
        # Crear país, estado y ciudad de prueba
        self.pais = Pais.objects.create(nombre='México')
        self.estado = Estado.objects.create(
            nombre='Baja California',
            pais=self.pais
        )
        self.ciudad_tecate = Ciudad.objects.create(
            nombre='Tecate',
            estado=self.estado
        )
        self.ciudad_tijuana = Ciudad.objects.create(
            nombre='Tijuana',
            estado=self.estado
        )
        
        # Crear equipos de prueba
        self.equipo_local = Equipo.objects.create(
            nombre='Cerveceros de Tecate',
            ciudad=self.ciudad_tecate
        )
        self.equipo_visitante = Equipo.objects.create(
            nombre='Toros de Tijuana',
            ciudad=self.ciudad_tijuana
        )
        
        # Crear jugadores de prueba
        self.jugador = Jugador.objects.create(
            nombre='Juan Pérez',
            numero=10,
            posicion='P',
            activo=True
        )
        
        # Crear partidos de prueba
        self.partido_futuro = Partido.objects.create(
            equipo_local=self.equipo_local,
            equipo_visitante=self.equipo_visitante,
            fecha=timezone.now() + timedelta(days=7),
            estado='programado'
        )
        
        self.partido_finalizado = Partido.objects.create(
            equipo_local=self.equipo_local,
            equipo_visitante=self.equipo_visitante,
            fecha=timezone.now() - timedelta(days=7),
            estado='finalizado',
            carreras_local=5,
            carreras_visitante=3
        )
        
        # Crear noticias de prueba
        self.noticia = Noticia.objects.create(
            titulo='Noticia de Prueba',
            contenido='Contenido de la noticia de prueba',
            fecha_publicacion=timezone.now(),
            destacada=True
        )

    # Tests de páginas principales
    def test_inicio_page_loads(self):
        """Test: La página de inicio carga correctamente"""
        response = self.client.get(reverse('equipo:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipo/inicio.html')

    def test_nuestro_equipo_page_loads(self):
        """Test: La página de nuestro equipo carga correctamente"""
        response = self.client.get(reverse('equipo:nuestro_equipo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipo/nuestro_equipo.html')
        self.assertIn('jugadores', response.context)

    def test_calendario_page_loads(self):
        """Test: La página de calendario carga correctamente"""
        response = self.client.get(reverse('equipo:calendario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipo/calendario.html')
        self.assertIn('calendario', response.context)
        self.assertIn('partidos_por_dia', response.context)

    def test_resultados_page_loads(self):
        """Test: La página de resultados carga correctamente"""
        response = self.client.get(reverse('equipo:resultados'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipo/resultados.html')
        self.assertIn('partidos', response.context)

    def test_noticias_page_loads(self):
        """Test: La página de noticias carga correctamente"""
        response = self.client.get(reverse('equipo:noticias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipo/noticias.html')
        self.assertIn('noticias', response.context)

    def test_tabla_posiciones_page_loads(self):
        """Test: La página de tabla de posiciones carga correctamente"""
        response = self.client.get(reverse('equipo:tabla_posiciones'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipo/tabla_posiciones.html')

    # Tests de funcionalidad del calendario
    def test_calendario_muestra_partidos(self):
        """Test: El calendario muestra los partidos correctamente"""
        response = self.client.get(reverse('equipo:calendario'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('partidos_por_dia', response.context)

    def test_calendario_navegacion_meses(self):
        """Test: La navegación entre meses del calendario funciona"""
        response = self.client.get(
            reverse('equipo:calendario') + '?mes=1&anio=2026'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['mes'], 1)
        self.assertEqual(response.context['anio'], 2026)

    # Tests de resultados
    def test_resultados_muestra_partidos_finalizados(self):
        """Test: La página de resultados muestra solo partidos finalizados"""
        response = self.client.get(reverse('equipo:resultados'))
        partidos = response.context['partidos']
        for partido in partidos:
            self.assertEqual(partido.estado, 'finalizado')

    # Tests de noticias
    def test_noticias_muestra_destacadas(self):
        """Test: Las noticias destacadas se muestran correctamente"""
        response = self.client.get(reverse('equipo:noticias'))
        noticias = response.context['noticias']
        destacadas = [n for n in noticias if n.destacada]
        self.assertGreater(len(destacadas), 0)

    def test_noticia_detalle_page_loads(self):
        """Test: La página de detalle de noticia carga correctamente"""
        response = self.client.get(
            reverse('equipo:noticia_detalle', args=[self.noticia.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipo/noticia_detalle.html')
        self.assertEqual(response.context['noticia'], self.noticia)

    # Tests de jugadores
    def test_jugador_detalle_page_loads(self):
        """Test: La página de detalle de jugador carga correctamente"""
        response = self.client.get(
            reverse('equipo:jugador_detalle', args=[self.jugador.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipo/jugador_detalle.html')
        self.assertEqual(response.context['jugador'], self.jugador)

    # Tests de internacionalización
    def test_i18n_espanol(self):
        """Test: El sitio funciona en español"""
        response = self.client.get(reverse('equipo:inicio'))
        self.assertEqual(response.status_code, 200)

    def test_i18n_ingles(self):
        """Test: El sitio funciona en inglés"""
        self.client.cookies.load({'django_language': 'en'})
        response = self.client.get(reverse('equipo:inicio'))
        self.assertEqual(response.status_code, 200)

    # Tests de URLs
    def test_all_main_urls_accessible(self):
        """Test: Todas las URLs principales son accesibles"""
        urls = [
            'equipo:inicio',
            'equipo:nuestro_equipo',
            'equipo:calendario',
            'equipo:resultados',
            'equipo:noticias',
            'equipo:tabla_posiciones',
        ]
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(
                response.status_code, 200,
                f"URL {url_name} no es accesible"
            )


class ModelsTestCase(TestCase):
    """Tests para los modelos"""

    def setUp(self):
        """Configuración inicial"""
        # Crear país, estado y ciudad de prueba
        self.pais = Pais.objects.create(nombre='Test Country')
        self.estado = Estado.objects.create(
            nombre='Test State',
            pais=self.pais
        )
        self.ciudad = Ciudad.objects.create(
            nombre='Test City',
            estado=self.estado
        )
        self.equipo = Equipo.objects.create(
            nombre='Test Team',
            ciudad=self.ciudad
        )

    def test_jugador_creation(self):
        """Test: Crear un jugador correctamente"""
        jugador = Jugador.objects.create(
            nombre='Test Player',
            numero=99,
            posicion='P',
            activo=True
        )
        self.assertEqual(str(jugador), '#99 Test Player')
        self.assertTrue(jugador.activo)

    def test_partido_creation(self):
        """Test: Crear un partido correctamente"""
        partido = Partido.objects.create(
            equipo_local=self.equipo,
            equipo_visitante=self.equipo,
            fecha=timezone.now(),
            estado='programado'
        )
        self.assertEqual(partido.estado, 'programado')

    def test_noticia_creation(self):
        """Test: Crear una noticia correctamente"""
        noticia = Noticia.objects.create(
            titulo='Test News',
            contenido='Test content',
            fecha_publicacion=timezone.now()
        )
        self.assertEqual(noticia.titulo, 'Test News')
        self.assertFalse(noticia.destacada)


class PanelCajaTransaccionFormTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='staff',
            password='pass12345',
            is_staff=True,
        )
        self.client.force_login(self.user)

    def _base_payload(self):
        now = timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M')
        return {
            'concepto': 'Venta boletos',
            'tipo': 'ingreso',
            'categoria': 'boletos',
            'monto': '100.00',
            'metodo_pago': 'efectivo',
            'fecha': now,
            'notas': 'test',
        }

    def test_guardar_transaccion_mxn_sin_tipo_cambio(self):
        payload = self._base_payload()
        payload.update({'moneda': 'MXN', 'tipo_cambio': ''})

        url = reverse('panel:transaccion_nueva')
        resp = self.client.post(url, payload)
        self.assertEqual(resp.status_code, 302)

        from .models import Transaccion

        t = Transaccion.objects.get(concepto='Venta boletos')
        self.assertEqual(t.moneda, 'MXN')
        self.assertIsNone(t.tipo_cambio)

    def test_guardar_transaccion_usd_con_tipo_cambio(self):
        payload = self._base_payload()
        payload.update({'moneda': 'USD', 'tipo_cambio': '18.500000'})

        url = reverse('panel:transaccion_nueva')
        resp = self.client.post(url, payload)
        self.assertEqual(resp.status_code, 302)

        from .models import Transaccion

        t = Transaccion.objects.get(concepto='Venta boletos')
        self.assertEqual(t.moneda, 'USD')
        self.assertIsNotNone(t.tipo_cambio)

    def test_usd_sin_tipo_cambio_usa_tc_global(self):
        payload = self._base_payload()
        payload.update({'moneda': 'USD', 'tipo_cambio': ''})

        url = reverse('panel:transaccion_nueva')
        resp = self.client.post(url, payload)
        self.assertEqual(resp.status_code, 302)

        from .models import Transaccion

        t = Transaccion.objects.get(concepto='Venta boletos')
        self.assertEqual(t.moneda, 'USD')
        self.assertIsNotNone(t.tipo_cambio)
        self.assertGreater(t.tipo_cambio, 0)
