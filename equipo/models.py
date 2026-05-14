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
    ciudad = models.CharField(max_length=100)
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
    
    class Meta:
        verbose_name_plural = "Partidos"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} - {self.fecha.strftime('%d/%m/%Y')}"


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    autor = models.CharField(max_length=100, blank=True)
    destacada = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Noticias"
        ordering = ['-fecha_publicacion']
    
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
    subtitulo = models.CharField(max_length=200, verbose_name="Subtítulo")
    titulo_linea1 = models.CharField(max_length=200, verbose_name="Título línea 1")
    titulo_linea2 = models.CharField(max_length=200, blank=True, verbose_name="Título línea 2")
    imagen = models.ImageField(upload_to='hero/', blank=True, null=True, verbose_name="Imagen (sube aquí)")
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

