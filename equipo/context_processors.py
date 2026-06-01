import re
import time
import urllib.request
import xml.etree.ElementTree as ET
import hashlib
import os
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from .models import Partido


# ==================== CONFIGURACIÓN ====================
RSS_URL = 'https://rss.app/feeds/hS2my7AUGemCdQkI.xml'
RSS_CACHE_TTL = 300  # segundos

_rss_cache = {
    'timestamp': 0,
    'items': [],
}


# ==================== FUNCIONES DE DESCARGA ====================
def download_instagram_image(image_url):
    """Descarga imagen de Instagram y la guarda localmente"""
    if not image_url:
        return None
    
    try:
        # Crear directorio de imágenes de Instagram si no existe
        instagram_dir = Path(settings.STATIC_ROOT) / 'images' / 'instagram'
        instagram_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar nombre único basado en hash de URL
        url_hash = hashlib.md5(image_url.encode()).hexdigest()
        filename = f"{url_hash}.jpg"
        filepath = instagram_dir / filename
        
        # Si ya existe, retornar la URL local
        if filepath.exists():
            return f'/static/images/instagram/{filename}'
        
        # Descargar imagen con headers para evitar bloqueos
        req = urllib.request.Request(
            image_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            image_data = response.read()
        
        # Guardar imagen localmente
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return f'/static/images/instagram/{filename}'
    
    except Exception:
# ==================== FUNCIONES DE RSS ====================
        return None


def fetch_instagram_rss_items(rss_url=None, max_items=6):
    if not getattr(settings, 'INSTAGRAM_RSS_ENABLED', True):
        return []

    rss_url = rss_url or getattr(settings, 'INSTAGRAM_RSS_URL', RSS_URL)
    now = time.time()
    if _rss_cache['items'] and now - _rss_cache['timestamp'] < RSS_CACHE_TTL:
        return _rss_cache['items'][:max_items]

    try:
        with urllib.request.urlopen(rss_url, timeout=10) as response:
            xml_content = response.read()
    except Exception:
        return []

    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return []

    items = []
    # Buscar más items del RSS para asegurar obtener max_items con imagen
    all_items = root.findall('.//item')
    for item in all_items:
        if len(items) >= max_items:
            break
            
        enlace = item.findtext('link') or '#'
        description = item.findtext('description') or ''
        match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', description)
        imagen_url = match.group(1) if match else ''
        
        if imagen_url:
            # Descargar y guardar localmente
            local_imagen_src = download_instagram_image(imagen_url)
            if local_imagen_src:
                items.append({'imagen_src': local_imagen_src, 'enlace': enlace})

    _rss_cache['timestamp'] = now
    _rss_cache['items'] = items
    return items[:max_items]

# ==================== CONTEXT PROCESSORS ====================

def instagram_footer_items(request):
    if not getattr(settings, 'INSTAGRAM_RSS_ENABLED', True):
        return {'footer_instagram_items': []}

    items = fetch_instagram_rss_items(max_items=6)
    if not items:
        items = [
            {'imagen_src': '/static/images/ig-footer-1.jpg', 'enlace': 'https://www.instagram.com/cervecerosdtecate/'},
            {'imagen_src': '/static/images/ig-footer-2.jpg', 'enlace': 'https://www.instagram.com/cervecerosdtecate/'},
            {'imagen_src': '/static/images/ig-footer-3.jpg', 'enlace': 'https://www.instagram.com/cervecerosdtecate/'},
            {'imagen_src': '/static/images/ig-footer-4.jpg', 'enlace': 'https://www.instagram.com/cervecerosdtecate/'},
            {'imagen_src': '/static/images/ig-footer-5.jpg', 'enlace': 'https://www.instagram.com/cervecerosdtecate/'},
            {'imagen_src': '/static/images/ig-footer-6.jpg', 'enlace': 'https://www.instagram.com/cervecerosdtecate/'},
        ]
    return {
        'footer_instagram_items': items,
    }


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

        fixtures.append(
            {
                'fecha': partido.fecha,
                'is_home': is_home,
                'opponent': opponent,
                'estadio': (partido.estadio or '').strip(),
                'local_nombre': local_nombre,
                'visitante_nombre': visitante_nombre,
                'local_logo': getattr(partido.equipo_local, 'logo_src', '') or '',
                'visitante_logo': getattr(partido.equipo_visitante, 'logo_src', '') or '',
            }
        )

    return {
        'footer_proximos_partidos': fixtures,
    }
