import re
import time
import threading
import urllib.request
import xml.etree.ElementTree as ET
import hashlib
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from .models import Partido


# ==================== CONFIGURACIÓN ====================
RSS_URL = 'https://rss.app/feeds/hS2my7AUGemCdQkI.xml'
RSS_CACHE_TTL = 120   # segundos entre refrescos del RSS
MAX_INSTAGRAM_ITEMS = 6

_rss_cache = {
    'timestamp': 0,
    'items': [],
}
_refresh_lock = threading.Lock()
_refresh_thread = None


# ==================== DESCARGA DE IMÁGENES ====================

_DOWNLOAD_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.instagram.com/',
}


def _get_instagram_dir():
    """Directorio local donde se guardan las imágenes descargadas."""
    static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
    base = Path(static_dirs[0]) if static_dirs else Path(settings.STATIC_ROOT)
    d = base / 'images' / 'instagram'
    d.mkdir(parents=True, exist_ok=True)
    return d


def download_instagram_image(image_url, post_url=''):
    """
    Descarga una imagen del CDN y la guarda en static/images/instagram/.
    Usa la URL del POST (estable) como clave de caché, no la URL del CDN
    (que cambia en cada llamada al RSS porque tiene firma con expiración).
    """
    if not image_url:
        return None
    try:
        instagram_dir = _get_instagram_dir()
        cache_key = post_url if post_url else image_url
        filename = hashlib.md5(cache_key.encode()).hexdigest() + '.jpg'
        filepath = instagram_dir / filename

        if filepath.exists() and filepath.stat().st_size > 0:
            return f'/static/images/instagram/{filename}'

        req = urllib.request.Request(image_url, headers=_DOWNLOAD_HEADERS)
        with urllib.request.urlopen(req, timeout=12) as response:
            image_data = response.read()

        if not image_data:
            return None

        filepath.write_bytes(image_data)
        return f'/static/images/instagram/{filename}'

    except Exception:
        return None


# ==================== LÓGICA RSS ====================

def _do_fetch(rss_url):
    """Descarga el RSS, procesa imágenes y actualiza el caché en memoria."""
    global _rss_cache

    try:
        req = urllib.request.Request(rss_url, headers=_DOWNLOAD_HEADERS)
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_content = response.read()
        root = ET.fromstring(xml_content)
    except Exception:
        return  # mantiene el caché anterior intacto

    items = []
    for item in root.findall('.//item'):
        if len(items) >= MAX_INSTAGRAM_ITEMS:
            break
        enlace = item.findtext('link') or '#'
        description = item.findtext('description') or ''
        match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', description)
        if not match:
            continue
        local_src = download_instagram_image(match.group(1), post_url=enlace)
        if local_src:
            items.append({'imagen_src': local_src, 'enlace': enlace})

    if items:
        _rss_cache['items'] = items
        _rss_cache['timestamp'] = time.time()


def _refresh_in_background(rss_url):
    """Hilo de fondo: refresca el caché sin bloquear el request."""
    global _refresh_thread
    try:
        _do_fetch(rss_url)
    finally:
        with _refresh_lock:
            _refresh_thread = None


def fetch_instagram_rss_items(max_items=MAX_INSTAGRAM_ITEMS):
    """
    Devuelve hasta max_items posts de Instagram.
    - Si el caché es fresco: respuesta instantánea.
    - Si el caché expiró Y hay datos anteriores: devuelve los anteriores
      mientras lanza un hilo de fondo para actualizar.
    - Si no hay caché (primer arranque): descarga sincrónicamente una vez.
    """
    global _refresh_thread

    if not getattr(settings, 'INSTAGRAM_RSS_ENABLED', True):
        return []

    rss_url = getattr(settings, 'INSTAGRAM_RSS_URL', RSS_URL)
    now = time.time()
    cache_fresh = _rss_cache['items'] and (now - _rss_cache['timestamp'] < RSS_CACHE_TTL)

    if cache_fresh:
        return _rss_cache['items'][:max_items]

    if _rss_cache['items']:
        # Hay datos anteriores: devolver mientras se actualiza en fondo
        with _refresh_lock:
            if _refresh_thread is None or not _refresh_thread.is_alive():
                _refresh_thread = threading.Thread(
                    target=_refresh_in_background,
                    args=(rss_url,),
                    daemon=True,
                )
                _refresh_thread.start()
        return _rss_cache['items'][:max_items]

    # Primera carga: bloquear hasta tener datos
    _do_fetch(rss_url)
    return _rss_cache['items'][:max_items]


def warm_cache():
    """Llama al arrancar el servidor para pre-cargar imágenes en segundo plano."""
    threading.Thread(target=fetch_instagram_rss_items, daemon=True).start()


# ==================== CONTEXT PROCESSORS ====================

def instagram_footer_items(request):
    if not getattr(settings, 'INSTAGRAM_RSS_ENABLED', True):
        return {'footer_instagram_items': []}

    IG_LINK = 'https://www.instagram.com/club_cervecerostecate/'
    TARGET = MAX_INSTAGRAM_ITEMS

    items = list(fetch_instagram_rss_items(max_items=TARGET))

    # Completar con imágenes del modelo ImagenInstagram si el RSS no alcanza 6
    if len(items) < TARGET:
        from .models import ImagenInstagram
        seen = {i['imagen_src'] for i in items}
        for db_item in ImagenInstagram.objects.filter(activo=True).order_by('orden'):
            if len(items) >= TARGET:
                break
            src = db_item.imagen_src
            if src and src not in seen:
                items.append({'imagen_src': src, 'enlace': db_item.enlace or IG_LINK})
                seen.add(src)

    # Si aún faltan, usar placeholders estáticos
    static_fallbacks = [
        {'imagen_src': '/static/images/ig-footer-1.jpg', 'enlace': IG_LINK},
        {'imagen_src': '/static/images/ig-footer-2.jpg', 'enlace': IG_LINK},
        {'imagen_src': '/static/images/ig-footer-3.jpg', 'enlace': IG_LINK},
        {'imagen_src': '/static/images/ig-footer-4.jpg', 'enlace': IG_LINK},
        {'imagen_src': '/static/images/ig-footer-5.jpg', 'enlace': IG_LINK},
        {'imagen_src': '/static/images/ig-footer-6.jpg', 'enlace': IG_LINK},
    ]
    idx = 0
    while len(items) < TARGET:
        items.append(static_fallbacks[idx % len(static_fallbacks)])
        idx += 1

    return {'footer_instagram_items': items[:TARGET]}


def footer_fixtures(request):
    proximos = (
        Partido.objects.filter(fecha__gte=timezone.now(), estado='programado')
        .select_related('equipo_local', 'equipo_visitante')
        .order_by('fecha')[:3]
    )

    fixtures = []
    for partido in proximos:
        local_nombre = (partido.equipo_local.nombre or '').strip()
        visitante_nombre = (partido.equipo_visitante.nombre or '').strip()

        local_is_cerveceros = 'cerveceros' in local_nombre.lower()
        visitante_is_cerveceros = 'cerveceros' in visitante_nombre.lower()

        if local_is_cerveceros and not visitante_is_cerveceros:
            is_home = True
            opponent = visitante_nombre
        elif visitante_is_cerveceros and not local_is_cerveceros:
            is_home = False
            opponent = local_nombre
        else:
            is_home = True
            opponent = visitante_nombre

        fixtures.append({
            'fecha': partido.fecha,
            'is_home': is_home,
            'opponent': opponent,
            'estadio': (partido.estadio or '').strip(),
            'local_nombre': local_nombre,
            'visitante_nombre': visitante_nombre,
            'local_logo': getattr(partido.equipo_local, 'logo_src', '') or '',
            'visitante_logo': getattr(partido.equipo_visitante, 'logo_src', '') or '',
        })

    return {'footer_proximos_partidos': fixtures}
