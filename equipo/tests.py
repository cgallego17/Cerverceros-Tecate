from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse


class UsuarioCrearTestCase(TestCase):
    """Tests para la creación de usuarios en el panel"""

    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear un superusuario para las pruebas
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='admin', password='testpass123')
        
        # Crear un grupo de prueba
        self.test_group = Group.objects.create(name='Test Role')

    def test_crear_usuario_basico(self):
        """Test: Crear un usuario básico sin roles"""
        response = self.client.post(reverse('panel:usuario_nuevo'), {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'is_staff': True,
            'is_active': True,
        })
        
        # Verificar redirección exitosa
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('panel:usuarios_lista'))
        
        # Verificar que el usuario fue creado
        user = User.objects.get(username='testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        
        # Verificar que la contraseña fue establecida correctamente
        self.assertTrue(user.check_password('SecurePass123!'))

    def test_crear_usuario_con_roles(self):
        """Test: Crear un usuario con roles asignados"""
        response = self.client.post(reverse('panel:usuario_nuevo'), {
            'username': 'userwithrole',
            'first_name': 'User',
            'last_name': 'WithRole',
            'email': 'role@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'is_staff': True,
            'is_active': True,
            'groups': [self.test_group.id],
        })
        
        # Verificar redirección exitosa
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario fue creado con el rol
        user = User.objects.get(username='userwithrole')
        self.assertIn(self.test_group, user.groups.all())

    def test_crear_usuario_contrasenas_no_coinciden(self):
        """Test: Error cuando las contraseñas no coinciden"""
        response = self.client.post(reverse('panel:usuario_nuevo'), {
            'username': 'testuser2',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'is_staff': True,
            'is_active': True,
        })
        
        # Verificar que no redirige (hay errores)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el usuario NO fue creado
        self.assertFalse(User.objects.filter(username='testuser2').exists())

    def test_crear_usuario_contrasena_debil(self):
        """Test: Error cuando la contraseña es demasiado débil"""
        response = self.client.post(reverse('panel:usuario_nuevo'), {
            'username': 'testuser3',
            'password1': '123',
            'password2': '123',
            'is_staff': True,
            'is_active': True,
        })
        
        # Verificar que no redirige (hay errores)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el usuario NO fue creado
        self.assertFalse(User.objects.filter(username='testuser3').exists())

    def test_crear_usuario_username_duplicado(self):
        """Test: Error cuando el username ya existe"""
        # Crear un usuario primero
        User.objects.create_user(
            username='existing',
            password='testpass123'
        )
        
        # Intentar crear otro con el mismo username
        response = self.client.post(reverse('panel:usuario_nuevo'), {
            'username': 'existing',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'is_staff': True,
            'is_active': True,
        })
        
        # Verificar que no redirige (hay errores)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que solo existe un usuario con ese username
        self.assertEqual(User.objects.filter(username='existing').count(), 1)

    def test_acceso_sin_permisos(self):
        """Test: Usuario no superusuario no puede crear usuarios"""
        # Crear un usuario staff pero no superusuario
        regular_user = User.objects.create_user(
            username='regular',
            password='testpass123'
        )
        regular_user.is_staff = True
        regular_user.save()
        
        # Cerrar sesión del superusuario
        self.client.logout()
        
        # Iniciar sesión con usuario regular
        self.client.login(username='regular', password='testpass123')
        
        # Intentar acceder a crear usuario
        response = self.client.get(reverse('panel:usuario_nuevo'))
        
        # Debe redirigir al dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('panel:dashboard'))

    def test_template_renderiza_correctamente(self):
        """Test: El template se renderiza sin errores"""
        response = self.client.get(reverse('panel:usuario_nuevo'))
        
        # Verificar que la página carga correctamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'panel/usuario_form.html')
        
        # Verificar que el formulario está en el contexto
        self.assertIn('form', response.context)
        
        # Verificar que contiene los campos esperados
        self.assertContains(response, 'username')
        self.assertContains(response, 'password1')
        self.assertContains(response, 'password2')
        self.assertContains(response, 'Crear usuario')
