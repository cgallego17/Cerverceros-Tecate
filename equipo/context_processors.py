import re
import time
import urllib.request
import xml.etree.ElementTree as ET

from django.conf import settings

RSS_URL = 'https://rss.app/feeds/hS2my7AUGemCdQkI.xml'
RSS_CACHE_TTL = 300  # segundos

_rss_cache = {
    'timestamp': 0,
    'items': [],
}


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
    for item in root.findall('.//item')[:max_items]:
        enlace = item.findtext('link') or '#'
        description = item.findtext('description') or ''
        match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', description)
        imagen_src = match.group(1) if match else ''
        if imagen_src:
            items.append({'imagen_src': imagen_src, 'enlace': enlace})

    _rss_cache['timestamp'] = now
    _rss_cache['items'] = items
    return items[:max_items]


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
