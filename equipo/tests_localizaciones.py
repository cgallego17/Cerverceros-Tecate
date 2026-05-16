from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from equipo.models import Pais, Estado, Ciudad


class LocalizacionesModelTestCase(TestCase):
    """Tests para los modelos de localizaciones"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.pais = Pais.objects.create(
            nombre='México',
            codigo='MEX',
            activo=True
        )
        self.estado = Estado.objects.create(
            pais=self.pais,
            nombre='Baja California',
            codigo='BC',
            activo=True
        )
        self.ciudad = Ciudad.objects.create(
            estado=self.estado,
            nombre='Tecate',
            activo=True
        )

    def test_crear_pais(self):
        """Test: Crear un país"""
        self.assertEqual(self.pais.nombre, 'México')
        self.assertEqual(self.pais.codigo, 'MEX')
        self.assertTrue(self.pais.activo)
        self.assertEqual(str(self.pais), 'México')

    def test_crear_estado(self):
        """Test: Crear un estado"""
        self.assertEqual(self.estado.nombre, 'Baja California')
        self.assertEqual(self.estado.codigo, 'BC')
        self.assertEqual(self.estado.pais, self.pais)
        self.assertTrue(self.estado.activo)
        self.assertEqual(str(self.estado), 'Baja California, México')

    def test_crear_ciudad(self):
        """Test: Crear una ciudad"""
        self.assertEqual(self.ciudad.nombre, 'Tecate')
        self.assertEqual(self.ciudad.estado, self.estado)
        self.assertTrue(self.ciudad.activo)
        self.assertEqual(str(self.ciudad), 'Tecate, Baja California')

    def test_ciudad_nombre_completo(self):
        """Test: Propiedad nombre_completo de ciudad"""
        nombre_completo = self.ciudad.nombre_completo
        self.assertEqual(nombre_completo, 'Tecate, Baja California, México')

    def test_relacion_pais_estados(self):
        """Test: Relación entre país y estados"""
        self.assertEqual(self.pais.estados.count(), 1)
        self.assertIn(self.estado, self.pais.estados.all())

    def test_relacion_estado_ciudades(self):
        """Test: Relación entre estado y ciudades"""
        self.assertEqual(self.estado.ciudades.count(), 1)
        self.assertIn(self.ciudad, self.estado.ciudades.all())

    def test_unique_codigo_pais(self):
        """Test: Código de país debe ser único"""
        with self.assertRaises(Exception):
            Pais.objects.create(nombre='Estados Unidos', codigo='MEX')

    def test_unique_estado_por_pais(self):
        """Test: Estado debe ser único por país"""
        with self.assertRaises(Exception):
            Estado.objects.create(
                pais=self.pais,
                nombre='Baja California',
                codigo='BC2'
            )

    def test_unique_ciudad_por_estado(self):
        """Test: Ciudad debe ser única por estado"""
        with self.assertRaises(Exception):
            Ciudad.objects.create(
                estado=self.estado,
                nombre='Tecate'
            )


class LocalizacionesViewTestCase(TestCase):
    """Tests para las vistas de localizaciones"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='admin', password='testpass123')

        self.pais = Pais.objects.create(
            nombre='México',
            codigo='MEX',
            activo=True
        )
        self.estado = Estado.objects.create(
            pais=self.pais,
            nombre='Baja California',
            codigo='BC',
            activo=True
        )
        self.ciudad = Ciudad.objects.create(
            estado=self.estado,
            nombre='Tecate',
            activo=True
        )

    def test_paises_lista_view(self):
        """Test: Vista de lista de países"""
        response = self.client.get(reverse('panel:paises_lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'México')
        self.assertContains(response, 'MEX')

    def test_crear_pais(self):
        """Test: Crear un país desde el panel"""
        response = self.client.post(reverse('panel:pais_nuevo'), {
            'nombre': 'Estados Unidos',
            'codigo': 'USA',
            'activo': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pais.objects.filter(codigo='USA').exists())

    def test_editar_pais(self):
        """Test: Editar un país"""
        response = self.client.post(
            reverse('panel:pais_editar', args=[self.pais.pk]),
            {
                'nombre': 'México Actualizado',
                'codigo': 'MEX',
                'activo': True,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.pais.refresh_from_db()
        self.assertEqual(self.pais.nombre, 'México Actualizado')

    def test_eliminar_pais(self):
        """Test: Eliminar un país"""
        pais_id = self.pais.pk
        response = self.client.post(
            reverse('panel:pais_eliminar', args=[pais_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pais.objects.filter(pk=pais_id).exists())

    def test_estados_lista_view(self):
        """Test: Vista de lista de estados"""
        response = self.client.get(reverse('panel:estados_lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Baja California')

    def test_crear_estado(self):
        """Test: Crear un estado desde el panel"""
        response = self.client.post(reverse('panel:estado_nuevo'), {
            'pais': self.pais.pk,
            'nombre': 'Sonora',
            'codigo': 'SON',
            'activo': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Estado.objects.filter(nombre='Sonora').exists())

    def test_ciudades_lista_view(self):
        """Test: Vista de lista de ciudades"""
        response = self.client.get(reverse('panel:ciudades_lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tecate')

    def test_crear_ciudad(self):
        """Test: Crear una ciudad desde el panel"""
        response = self.client.post(reverse('panel:ciudad_nueva'), {
            'estado': self.estado.pk,
            'nombre': 'Tijuana',
            'activo': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ciudad.objects.filter(nombre='Tijuana').exists())

    def test_acceso_sin_permisos(self):
        """Test: Usuario sin permisos no puede acceder"""
        self.client.logout()
        
        regular_user = User.objects.create_user(
            username='regular',
            password='testpass123'
        )
        self.client.login(username='regular', password='testpass123')
        
        response = self.client.get(reverse('panel:paises_lista'))
        self.assertEqual(response.status_code, 302)


class PoblarMexicoTestCase(TestCase):
    """Tests para verificar el poblado de México"""

    def test_mexico_poblado_completo(self):
        """Test: Verificar que México está poblado correctamente"""
        # Ejecutar el script de poblado
        from poblar_mexico import poblar_mexico
        poblar_mexico()
        
        # Verificar que México existe
        mexico = Pais.objects.get(codigo='MEX')
        self.assertEqual(mexico.nombre, 'México')
        
        # Verificar que tiene 32 estados
        self.assertEqual(mexico.estados.count(), 32)
        
        # Verificar que Baja California existe
        bc = Estado.objects.get(pais=mexico, nombre='Baja California')
        self.assertTrue(bc.ciudades.filter(nombre='Tecate').exists())
        
        # Verificar que hay ciudades
        total_ciudades = Ciudad.objects.filter(estado__pais=mexico).count()
        self.assertGreater(total_ciudades, 100)

    def test_estados_principales(self):
        """Test: Verificar que los estados principales existen"""
        from poblar_mexico import poblar_mexico
        poblar_mexico()
        
        mexico = Pais.objects.get(codigo='MEX')
        
        estados_esperados = [
            'Baja California',
            'Nuevo León',
            'Jalisco',
            'Ciudad de México',
            'Quintana Roo'
        ]
        
        for nombre_estado in estados_esperados:
            self.assertTrue(
                Estado.objects.filter(pais=mexico, nombre=nombre_estado).exists(),
                f"Estado {nombre_estado} no encontrado"
            )

    def test_ciudades_principales(self):
        """Test: Verificar que las ciudades principales existen"""
        from poblar_mexico import poblar_mexico
        poblar_mexico()
        
        mexico = Pais.objects.get(codigo='MEX')
        
        ciudades_esperadas = [
            ('Baja California', 'Tijuana'),
            ('Baja California', 'Tecate'),
            ('Nuevo León', 'Monterrey'),
            ('Jalisco', 'Guadalajara'),
            ('Quintana Roo', 'Cancún'),
        ]
        
        for nombre_estado, nombre_ciudad in ciudades_esperadas:
            estado = Estado.objects.get(pais=mexico, nombre=nombre_estado)
            self.assertTrue(
                Ciudad.objects.filter(estado=estado, nombre=nombre_ciudad).exists(),
                f"Ciudad {nombre_ciudad} en {nombre_estado} no encontrada"
            )
