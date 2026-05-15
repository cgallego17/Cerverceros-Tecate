"""Gunicorn configuration file"""
import multiprocessing

# Bind
bind = "127.0.0.1:8000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "cerveceros_tecate"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/cerveceros.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None

# SSL (opcional, si usas HTTPS directamente en Gunicorn)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
