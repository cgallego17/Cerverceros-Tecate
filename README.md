# Cerveceros de Tecate - Aplicación Web

Aplicación web desarrollada en Django para el equipo de baseball **Cerveceros de Tecate**.

## Características

La aplicación incluye las siguientes páginas:

- **Inicio**: Página principal con noticias destacadas, próximos partidos y últimos resultados
- **Nuestro Equipo**: Roster completo de jugadores con sus perfiles
- **Calendario**: Calendario completo de partidos de la temporada
- **Resultados**: Resultados de los partidos finalizados
- **Tabla de Posiciones**: Clasificación de la liga
- **Noticias**: Todas las noticias del equipo
- **Boletería**: Sistema de venta de boletos para los partidos

## Colores del Equipo

- **Rojo**: #DC143C
- **Negro**: #1a1a1a
- **Blanco**: #ffffff

## Requisitos

- Python 3.8 o superior
- Django 4.2.7
- Pillow 10.1.0

## Instalación

### 1. Crear un entorno virtual

```bash
python -m venv venv
```

### 2. Activar el entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Realizar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear un superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu cuenta de administrador.

### 6. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

## Panel de Administración

Accede al panel de administración en: `http://127.0.0.1:8000/admin/`

Desde aquí podrás:
- Agregar y gestionar jugadores
- Crear equipos
- Programar partidos
- Publicar noticias
- Configurar boletos
- Actualizar la tabla de posiciones

## Estructura del Proyecto

```
Cerverceros Tecate/
├── cerveceros_tecate/      # Configuración principal del proyecto
│   ├── settings.py         # Configuración de Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuración WSGI
├── equipo/                # Aplicación principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas
│   ├── urls.py            # URLs de la app
│   └── admin.py           # Configuración del admin
├── templates/             # Plantillas HTML
│   └── equipo/
├── static/               # Archivos estáticos
│   └── css/
│       └── styles.css    # Estilos CSS
├── media/                # Archivos subidos (se crea automáticamente)
├── manage.py             # Script de gestión de Django
└── requirements.txt      # Dependencias del proyecto
```

## Modelos de Datos

### Jugador
- Información personal del jugador
- Número, posición, foto
- Estadísticas básicas

### Equipo
- Nombre y ciudad del equipo
- Logo

### Partido
- Equipos local y visitante
- Fecha y hora
- Marcador
- Estado (programado, en curso, finalizado)

### Noticia
- Título y contenido
- Imagen
- Fecha de publicación
- Marcador de destacada

### Boleto
- Tipo (general, preferente, VIP, palco)
- Precio
- Cantidad disponible
- Asociado a un partido

### TablaPosiciones
- Estadísticas del equipo en la temporada
- Juegos jugados, ganados, perdidos
- Porcentaje de victorias
- Carreras a favor y en contra

## Uso

1. Accede al panel de administración
2. Crea el equipo "Cerveceros de Tecate"
3. Agrega jugadores al roster
4. Crea equipos rivales
5. Programa partidos
6. Publica noticias
7. Configura boletos para los partidos
8. Actualiza la tabla de posiciones

## Personalización

Los estilos se encuentran en `static/css/styles.css`. Puedes modificar los colores y diseño según tus necesidades.

## Producción

Para desplegar en producción:

1. Cambia `DEBUG = False` en `settings.py`
2. Configura `ALLOWED_HOSTS` con tu dominio
3. Cambia `SECRET_KEY` por una clave segura
4. Configura una base de datos de producción (PostgreSQL recomendado)
5. Ejecuta `python manage.py collectstatic`
6. Configura un servidor web (Nginx + Gunicorn recomendado)

## Soporte

Para cualquier duda o problema, contacta al equipo de desarrollo.

---

**¡Vamos Cerveceros de Tecate!** 🍺⚾
