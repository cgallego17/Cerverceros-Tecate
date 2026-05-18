from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Jugador(models.Model):
    POSICIONES = [
        ('P', 'Pitcher'),
        ('C', 'Catcher'),
        ('1B', 'Primera Base'),
        ('2B', 'Segunda Base'),
        ('3B', 'Tercera Base'),
        ('SS', 'Shortstop'),
        ('LF', 'Left Field'),
        ('CF', 'Center Field'),
        ('RF', 'Right Field'),
        ('DH', 'Designated Hitter'),
    ]
    
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()
    posicion = models.CharField(max_length=2, choices=POSICIONES)
    foto = models.ImageField(upload_to='jugadores/', blank=True, null=True)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    altura = models.CharField(max_length=20, blank=True)
    peso = models.CharField(max_length=20, blank=True)
    bateo = models.CharField(max_length=10, blank=True)
    lanzamiento = models.CharField(max_length=10, blank=True)
    activo = models.BooleanField(default=True)
    destacado_inicio = models.BooleanField(
        default=False,
        verbose_name="Destacar en inicio",
        help_text="Mostrar este jugador en la sección destacada del inicio"
    )
    
    class Meta:
        verbose_name_plural = "Jugadores"
        ordering = ['numero']
    
    def __str__(self):
        return f"#{self.numero} {self.nombre}"


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.ForeignKey('Ciudad', on_delete=models.SET_NULL, null=True, blank=True, related_name='equipos', verbose_name='Ciudad')
    logo = models.ImageField(upload_to='equipos/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Equipos"
    
    def __str__(self):
        return self.nombre


class Partido(models.Model):
    ESTADOS = [
        ('programado', 'Programado'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
        ('pospuesto', 'Pospuesto'),
        ('cancelado', 'Cancelado'),
    ]
    
    fecha = models.DateTimeField()
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    carreras_local = models.IntegerField(default=0)
    carreras_visitante = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='programado')
    estadio = models.CharField(max_length=200, blank=True)
    temporada = models.CharField(max_length=20)
    destacado = models.BooleanField(default=False, verbose_name='Próximo partido destacado', help_text='Marcar como el próximo partido a mostrar en la página de inicio')
    imagen_fondo = models.ImageField(upload_to='partidos/', blank=True, null=True, verbose_name='Imagen de fondo', help_text='Imagen de fondo para la sección de próximo partido')
    opacidad_overlay = models.DecimalField(max_digits=3, decimal_places=2, default=0.60, verbose_name='Opacidad del overlay', help_text='Opacidad del overlay oscuro (0.00 = transparente, 1.00 = opaco)')
    
    class Meta:
        verbose_name_plural = "Partidos"
        ordering = ['-fecha']
    
    def save(self, *args, **kwargs):
        if self.destacado:
            Partido.objects.filter(destacado=True).exclude(pk=self.pk).update(destacado=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} - {self.fecha.strftime('%d/%m/%Y')}"


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    autor = models.CharField(max_length=100, blank=True)
    destacada = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Noticias"
        ordering = ['-fecha_publicacion']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titulo


class Boleto(models.Model):
    TIPOS = [
        ('general', 'General'),
        ('preferente', 'Preferente'),
        ('vip', 'VIP'),
        ('palco', 'Palco'),
    ]
    
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='boletos')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField(default=0)
    seccion = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = "Boletos"
    
    def __str__(self):
        return f"{self.tipo} - {self.partido}"


class TablaPosiciones(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    temporada = models.CharField(max_length=20)
    juegos_jugados = models.IntegerField(default=0)
    ganados = models.IntegerField(default=0)
    perdidos = models.IntegerField(default=0)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=3, default=0.000)
    carreras_favor = models.IntegerField(default=0)
    carreras_contra = models.IntegerField(default=0)
    racha = models.CharField(max_length=10, blank=True)
    
    class Meta:
        verbose_name_plural = "Tabla de Posiciones"
        ordering = ['-porcentaje', '-ganados']
    
    def __str__(self):
        return f"{self.equipo} - {self.temporada}"
    
    def save(self, *args, **kwargs):
        if self.juegos_jugados > 0:
            self.porcentaje = self.ganados / self.juegos_jugados
        super().save(*args, **kwargs)


# ──────────────────────────────────────────────
#  HOME – HERO SLIDER
# ──────────────────────────────────────────────

class HeroSlide(models.Model):
    subtitulo = models.CharField(max_length=200, blank=True, verbose_name="Subtítulo")
    titulo_linea1 = models.CharField(max_length=200, blank=True, verbose_name="Título línea 1")
    titulo_linea2 = models.CharField(max_length=200, blank=True, verbose_name="Título línea 2")
    imagen = models.ImageField(upload_to='hero/', verbose_name="Imagen (sube aquí)")
    imagen_url = models.URLField(blank=True, verbose_name="URL de imagen externa", help_text="Se usa si no subes imagen")
    btn1_texto = models.CharField(max_length=100, blank=True, verbose_name="Botón 1 texto")
    btn1_url = models.CharField(max_length=200, blank=True, verbose_name="Botón 1 enlace")
    btn2_texto = models.CharField(max_length=100, blank=True, verbose_name="Botón 2 texto")
    btn2_url = models.CharField(max_length=200, blank=True, verbose_name="Botón 2 enlace")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Diapositiva Hero"
        verbose_name_plural = "Diapositivas Hero"
        ordering = ['orden']

    def __str__(self):
        return f"{self.titulo_linea1} {self.titulo_linea2}".strip()

    @property
    def imagen_bg(self):
        """Returns the background URL (uploaded image takes priority)."""
        if self.imagen:
            return self.imagen.url
        return self.imagen_url or ''


# ──────────────────────────────────────────────
#  HOME – PATROCINADORES
# ──────────────────────────────────────────────

class Patrocinador(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    logo = models.ImageField(upload_to='patrocinadores/', blank=True, null=True, verbose_name="Logo")
    url = models.URLField(blank=True, verbose_name="Enlace web")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Patrocinador"
        verbose_name_plural = "Patrocinadores"
        ordering = ['orden']

    def __str__(self):
        return self.nombre


# ──────────────────────────────────────────────
#  MÓDULO DE PRODUCTOS
# ──────────────────────────────────────────────

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Producto(models.Model):
    BADGE_CHOICES = [
        ('', 'Sin etiqueta'),
        ('sale', 'Oferta'),
        ('new', 'Nuevo'),
        ('sold', 'Agotado'),
    ]

    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    categoria = models.ForeignKey(
        CategoriaProducto, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="Categoría"
    )
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio actual")
    precio_anterior = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True, verbose_name="Precio anterior (tachado)"
    )
    badge = models.CharField(max_length=10, choices=BADGE_CHOICES, blank=True, verbose_name="Etiqueta")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    destacado = models.BooleanField(
        default=False, verbose_name="Destacado en inicio",
        help_text="Mostrar en el carrusel de tienda del inicio"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def tiene_descuento(self):
        return self.precio_anterior is not None and self.precio_anterior > self.precio


# ──────────────────────────────────────────────
#  HOME – SECCIÓN FAQ / ACORDEÓN
# ──────────────────────────────────────────────

class ItemFaq(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    contenido = models.TextField(verbose_name="Contenido")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Pregunta Frecuente"
        verbose_name_plural = "Preguntas Frecuentes (FAQ)"
        ordering = ['orden']

    def __str__(self):
        return self.titulo


# ──────────────────────────────────────────────
#  HOME – SKILLS PROGRESS
# ──────────────────────────────────────────────

class SkillProgress(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la habilidad")
    porcentaje = models.PositiveIntegerField(
        default=0, 
        verbose_name="Porcentaje (0-100)",
        help_text="Valor entre 0 y 100"
    )
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Barra de Progreso"
        verbose_name_plural = "Barras de Progreso (Skills)"
        ordering = ['orden']

    def __str__(self):
        return f"{self.nombre} - {self.porcentaje}%"


# ──────────────────────────────────────────────
#  HOME – ARTÍCULOS DE NOTICIAS (NEWS GRID)
# ──────────────────────────────────────────────

class ArticuloNoticia(models.Model):
    TIPO_CHOICES = [
        ('texto', 'Solo Texto'),
        ('imagen', 'Con Imagen'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='texto', verbose_name="Tipo")
    imagen = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Imagen")
    enlace = models.CharField(max_length=200, blank=True, verbose_name="Enlace")
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    destacado_grid = models.BooleanField(
        default=False,
        verbose_name="Mostrar en News Grid",
        help_text="Mostrar en la sección de noticias del inicio"
    )

    class Meta:
        verbose_name = "Artículo de Noticia"
        verbose_name_plural = "Artículos de Noticias (News Grid)"
        ordering = ['orden']

    def __str__(self):
        return self.titulo


# ──────────────────────────────────────────────
#  HOME – IMÁGENES DE INSTAGRAM
# ──────────────────────────────────────────────

class ImagenInstagram(models.Model):
    imagen = models.ImageField(upload_to='instagram/', blank=True, null=True, verbose_name="Imagen")
    imagen_url = models.URLField(blank=True, verbose_name="URL de imagen", help_text="URL externa si no subes imagen")
    enlace = models.URLField(blank=True, verbose_name="Enlace a Instagram")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Imagen de Instagram"
        verbose_name_plural = "Imágenes de Instagram"
        ordering = ['orden']

    def __str__(self):
        return f"Instagram #{self.orden}"
    
    @property
    def imagen_src(self):
        if self.imagen:
            return self.imagen.url
        return self.imagen_url or ''


# ──────────────────────────────────────────────
#  CAJA REGISTRADORA
# ──────────────────────────────────────────────

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso',  'Egreso'),
    ]
    CATEGORIA_CHOICES = [
        ('boletos',      'Boletos'),
        ('tienda',       'Tienda'),
        ('patrocinios',  'Patrocinios'),
        ('nomina',       'Nómina'),
        ('operaciones',  'Operaciones'),
        ('otro',         'Otro'),
    ]
    METODO_CHOICES = [
        ('efectivo',      'Efectivo'),
        ('tarjeta',       'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('otro',          'Otro'),
    ]

    concepto      = models.CharField(max_length=200, verbose_name='Concepto')
    tipo          = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name='Tipo')
    categoria     = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='otro', verbose_name='Categoría')
    monto         = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto')
    metodo_pago   = models.CharField(max_length=20, choices=METODO_CHOICES, default='efectivo', verbose_name='Método de pago')
    fecha         = models.DateTimeField(default=timezone.now, verbose_name='Fecha')
    notas         = models.TextField(blank=True, verbose_name='Notas')
    registrado_por = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='transacciones', verbose_name='Registrado por'
    )

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} – {self.concepto} (${self.monto})"


class UserProfile(models.Model):
    """Perfil extendido de usuario con imagen"""
    from django.contrib.auth.models import User
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    @property
    def avatar_url(self):
        """Retorna la URL del avatar o un placeholder"""
        if self.avatar:
            return self.avatar.url
        return None


# ──────────────────────────────────────────────
#  LOCALIZACIONES
# ──────────────────────────────────────────────

class Pais(models.Model):
    """País para sistema de localizaciones"""
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=3, unique=True, help_text="Código ISO (ej: MEX, USA)")
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Estado(models.Model):
    """Estado o provincia"""
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='estados')
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, blank=True, help_text="Código del estado (ej: BC, NL)")
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['pais', 'nombre']
        unique_together = [['pais', 'nombre']]
    
    def __str__(self):
        return f"{self.nombre}, {self.pais.nombre}"


class Ciudad(models.Model):
    """Ciudad o municipio"""
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='ciudades')
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['estado', 'nombre']
        unique_together = [['estado', 'nombre']]
    
    def __str__(self):
        return f"{self.nombre}, {self.estado.nombre}"
    
    @property
    def nombre_completo(self):
        """Retorna nombre completo con estado y país"""
        return f"{self.nombre}, {self.estado.nombre}, {self.estado.pais.nombre}"


# ──────────────────────────────────────────────
#  HOME – PRÓXIMO JUEGO DESTACADO
# ──────────────────────────────────────────────

class ProximoJuegoDestacado(models.Model):
    """Sección de próximo juego destacado en la página de inicio"""
    activo = models.BooleanField(default=True, verbose_name="Activo")
    subtitulo = models.CharField(max_length=200, default="LO QUE ESTÁ EN TENDENCIA", verbose_name="Subtítulo")
    titulo = models.CharField(max_length=200, default="PRÓXIMO JUEGO", verbose_name="Título")
    partido = models.ForeignKey(Partido, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Partido")
    texto_personalizado = models.CharField(max_length=300, blank=True, verbose_name="Texto personalizado", help_text="Opcional: texto en lugar de mostrar equipos del partido")
    imagen_fondo = models.ImageField(upload_to='proximo_juego/', blank=True, null=True, verbose_name="Imagen de fondo")
    opacidad_overlay = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.70,
        verbose_name="Opacidad del overlay",
        help_text="0.00 = transparente, 1.00 = completamente opaco"
    )
    texto_boton = models.CharField(max_length=100, default="COMPRAR BOLETOS", verbose_name="Texto del botón")
    url_boton = models.URLField(default="https://arema.mx/e/17890", verbose_name="URL del botón")
    mostrar_countdown = models.BooleanField(default=True, verbose_name="Mostrar contador regresivo")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    
    class Meta:
        verbose_name = 'Próximo Juego Destacado'
        verbose_name_plural = 'Próximos Juegos Destacados'
        ordering = ['-activo', 'orden']
    
    def __str__(self):
        if self.partido:
            return f"Próximo Juego: {self.partido.equipo_local} vs {self.partido.equipo_visitante}"
        return f"Próximo Juego: {self.titulo}"
