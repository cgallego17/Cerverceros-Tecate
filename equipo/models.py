from django.db import models
from django.utils import timezone


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
