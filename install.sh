#!/usr/bin/env bash
# =============================================================================
#  Cerveceros de Tecate — Script de Instalación Automática
#  Dominio  : cervecerosdetecate.com
#  Servidor : Ubuntu 22.04 LTS (DigitalOcean)
#  Uso      : sudo bash install.sh
# =============================================================================

set -euo pipefail

# ── Colores ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

log()     { echo -e "${GREEN}[✔]${NC} $*"; }
info()    { echo -e "${BLUE}[→]${NC} $*"; }
warn()    { echo -e "${YELLOW}[!]${NC} $*"; }
section() { echo -e "\n${BOLD}${CYAN}══════════════════════════════════════════${NC}"; \
            echo -e "${BOLD}${CYAN}  $*${NC}"; \
            echo -e "${BOLD}${CYAN}══════════════════════════════════════════${NC}\n"; }
die()     { echo -e "${RED}[✘] ERROR: $*${NC}" >&2; exit 1; }

# ── Constantes ────────────────────────────────────────────────────────────────
DOMAIN="cervecerosdetecate.com"
WWW_DOMAIN="www.cervecerosdetecate.com"
REPO_URL="https://github.com/cgallego17/Cerverceros-Tecate.git"
DEPLOY_USER="deploy"
PROJECT_DIR="/home/${DEPLOY_USER}/cerveceros_tecate"
VENV_DIR="${PROJECT_DIR}/venv"
PYTHON_BIN="${VENV_DIR}/bin/python"
PIP_BIN="${VENV_DIR}/bin/pip"
GUNICORN_BIN="${VENV_DIR}/bin/gunicorn"
DB_NAME="cerveceros_db"
DB_USER="cerveceros_user"
NGINX_CONF="/etc/nginx/sites-available/cerveceros"
GUNICORN_SERVICE="/etc/systemd/system/gunicorn.service"
LOG_DIR="/var/log/gunicorn"

# ── Verificaciones previas ────────────────────────────────────────────────────
[[ $EUID -ne 0 ]] && die "Ejecuta el script como root: sudo bash install.sh"

section "Cerveceros de Tecate — Instalador"
echo -e "  Dominio    : ${BOLD}${DOMAIN}${NC}"
echo -e "  Proyecto   : ${BOLD}${PROJECT_DIR}${NC}"
echo -e "  Repositorio: ${BOLD}${REPO_URL}${NC}"
echo ""

# ── Solicitar datos sensibles ─────────────────────────────────────────────────
section "1 · Configuración inicial"

read -rsp "$(echo -e "${YELLOW}Contraseña para la base de datos PostgreSQL:${NC} ")" DB_PASSWORD
echo ""
[[ -z "$DB_PASSWORD" ]] && die "La contraseña de la BD no puede estar vacía."

read -rp "$(echo -e "${YELLOW}Nombre del superusuario Django:${NC} ")" ADMIN_USER
ADMIN_USER="${ADMIN_USER:-admin}"

read -rsp "$(echo -e "${YELLOW}Contraseña del superusuario Django:${NC} ")" ADMIN_PASS
echo ""
[[ -z "$ADMIN_PASS" ]] && die "La contraseña del superusuario no puede estar vacía."

read -rp "$(echo -e "${YELLOW}Email del superusuario Django:${NC} ")" ADMIN_EMAIL
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@${DOMAIN}}"

echo ""
log "Datos recibidos. Iniciando instalación..."

# ── Paso 1: Actualizar sistema ────────────────────────────────────────────────
section "2 · Actualizar sistema"
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get upgrade -y -qq
log "Sistema actualizado."

# ── Paso 2: Instalar dependencias del sistema ─────────────────────────────────
section "3 · Dependencias del sistema"
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    python3.11 python3.11-venv python3-pip \
    nginx \
    postgresql postgresql-contrib \
    git curl \
    libjpeg-dev zlib1g-dev libpq-dev \
    certbot python3-certbot-nginx \
    ufw \
    fail2ban
log "Dependencias instaladas."

# ── Paso 3: Crear usuario deploy ──────────────────────────────────────────────
section "4 · Usuario deploy"
if id "${DEPLOY_USER}" &>/dev/null; then
    warn "El usuario '${DEPLOY_USER}' ya existe. Continuando..."
else
    adduser --disabled-password --gecos "" "${DEPLOY_USER}"
    usermod -aG sudo "${DEPLOY_USER}"
    log "Usuario '${DEPLOY_USER}' creado."
fi

# ── Paso 4: Configurar PostgreSQL ─────────────────────────────────────────────
section "5 · PostgreSQL"
systemctl start postgresql
systemctl enable postgresql

# Crear usuario y BD de forma idempotente
sudo -u postgres psql -tc "SELECT 1 FROM pg_user WHERE usename='${DB_USER}'" \
    | grep -q 1 && warn "Usuario DB ya existe." || \
    sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" \
    | grep -q 1 && warn "Base de datos ya existe." || \
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

sudo -u postgres psql -c "
ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';
ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';
ALTER ROLE ${DB_USER} SET timezone TO 'America/Tijuana';
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
"
log "PostgreSQL configurado."

# ── Paso 5: Clonar proyecto ───────────────────────────────────────────────────
section "6 · Clonar repositorio"
if [[ -d "${PROJECT_DIR}/.git" ]]; then
    warn "El repositorio ya existe. Actualizando con git pull..."
    sudo -u "${DEPLOY_USER}" git -C "${PROJECT_DIR}" pull origin main
else
    sudo -u "${DEPLOY_USER}" git clone "${REPO_URL}" "${PROJECT_DIR}"
    log "Repositorio clonado en ${PROJECT_DIR}"
fi

# ── Paso 6: Entorno virtual y dependencias ────────────────────────────────────
section "7 · Entorno virtual Python"
if [[ ! -d "${VENV_DIR}" ]]; then
    sudo -u "${DEPLOY_USER}" python3.11 -m venv "${VENV_DIR}"
fi
sudo -u "${DEPLOY_USER}" "${PIP_BIN}" install --upgrade pip -q
sudo -u "${DEPLOY_USER}" "${PIP_BIN}" install -r "${PROJECT_DIR}/requirements.txt" -q
log "Dependencias Python instaladas."

# ── Paso 7: Generar SECRET_KEY y crear .env ───────────────────────────────────
section "8 · Archivo .env"
SECRET_KEY=$(sudo -u "${DEPLOY_USER}" "${PYTHON_BIN}" -c \
    "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

# Obtener IP pública del servidor
SERVER_IP=$(curl -s --max-time 5 https://api.ipify.org || echo "")

ALLOWED_HOSTS="${DOMAIN},${WWW_DOMAIN}"
[[ -n "$SERVER_IP" ]] && ALLOWED_HOSTS="${ALLOWED_HOSTS},${SERVER_IP}"

cat > "${PROJECT_DIR}/.env" <<EOF
# Django
SECRET_KEY=${SECRET_KEY}
DEBUG=False
ALLOWED_HOSTS=${ALLOWED_HOSTS}

# Base de datos
DB_ENGINE=django.db.backends.postgresql
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=localhost
DB_PORT=5432
EOF

chown "${DEPLOY_USER}:${DEPLOY_USER}" "${PROJECT_DIR}/.env"
chmod 600 "${PROJECT_DIR}/.env"
log "Archivo .env creado."

# ── Paso 8: Django — migraciones, estáticos, superusuario ────────────────────
section "9 · Configuración Django"

cd "${PROJECT_DIR}"

info "Ejecutando migraciones..."
sudo -u "${DEPLOY_USER}" "${PYTHON_BIN}" manage.py migrate --noinput

info "Recolectando archivos estáticos..."
sudo -u "${DEPLOY_USER}" "${PYTHON_BIN}" manage.py collectstatic --noinput -v 0

info "Compilando mensajes de traducción..."
sudo -u "${DEPLOY_USER}" "${PYTHON_BIN}" manage.py compilemessages 2>/dev/null || true

info "Creando carpetas de media..."
sudo -u "${DEPLOY_USER}" mkdir -p "${PROJECT_DIR}/media/"{jugadores,equipos,noticias,hero,patrocinadores,productos,news,instagram}

info "Creando superusuario..."
# printf %q escapa caracteres especiales (', ", $, etc.) de forma segura
_SU_USER=$(printf '%q' "${ADMIN_USER}")
_SU_PASS=$(printf '%q' "${ADMIN_PASS}")
_SU_EMAIL=$(printf '%q' "${ADMIN_EMAIL}")
sudo -u "${DEPLOY_USER}" bash -c "
    export DJANGO_SUPERUSER_USERNAME=${_SU_USER}
    export DJANGO_SUPERUSER_EMAIL=${_SU_EMAIL}
    export DJANGO_SUPERUSER_PASSWORD=${_SU_PASS}
    cd '${PROJECT_DIR}'
    '${PYTHON_BIN}' manage.py createsuperuser --no-input 2>/dev/null \
        && echo 'Superusuario creado.' \
        || echo 'El superusuario ya existe (omitido).'"

log "Django configurado."

# ── Paso 9: Logs de Gunicorn ──────────────────────────────────────────────────
section "10 · Gunicorn"
mkdir -p "${LOG_DIR}"
chown -R "${DEPLOY_USER}:www-data" "${LOG_DIR}"
chmod -R 775 "${LOG_DIR}"

# Servicio systemd
cat > "${GUNICORN_SERVICE}" <<EOF
[Unit]
Description=Gunicorn daemon — Cerveceros de Tecate
After=network.target

[Service]
User=${DEPLOY_USER}
Group=www-data
WorkingDirectory=${PROJECT_DIR}
Environment="PATH=${VENV_DIR}/bin"
ExecStart=${GUNICORN_BIN} \\
    --workers 3 \\
    --bind 127.0.0.1:8000 \\
    --timeout 60 \\
    --access-logfile ${LOG_DIR}/access.log \\
    --error-logfile ${LOG_DIR}/error.log \\
    cerveceros_tecate.wsgi:application
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable gunicorn
systemctl restart gunicorn
log "Gunicorn activo."

# ── Paso 10: Nginx ────────────────────────────────────────────────────────────
section "11 · Nginx (HTTP provisional para Certbot)"

# ── Paso 11: SSL con Let's Encrypt ───────────────────────────────────────────
section "12 · SSL — Let's Encrypt"

# Crear nginx temporal sin SSL para que certbot pueda verificar el dominio
cat > "${NGINX_CONF}" <<EOF
server {
    listen 80;
    server_name ${DOMAIN} ${WWW_DOMAIN};

    location /.well-known/acme-challenge/ { root /var/www/html; }

    location /static/ {
        alias ${PROJECT_DIR}/staticfiles/;
    }

    location /media/ {
        alias ${PROJECT_DIR}/media/;
    }

    location / {
        proxy_pass        http://127.0.0.1:8000;
        proxy_set_header  Host            \$host;
        proxy_set_header  X-Real-IP       \$remote_addr;
        proxy_set_header  X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto \$scheme;
    }

    access_log /var/log/nginx/cerveceros_access.log;
    error_log  /var/log/nginx/cerveceros_error.log;
}
EOF

# Activar sitio
ln -sf "${NGINX_CONF}" /etc/nginx/sites-enabled/cerveceros
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl restart nginx

info "Obteniendo certificado SSL para ${DOMAIN} y ${WWW_DOMAIN}..."
if certbot --nginx \
       -d "${DOMAIN}" \
       -d "${WWW_DOMAIN}" \
       --non-interactive \
       --agree-tos \
       --email "admin@${DOMAIN}" \
       --redirect; then

    log "Certificado SSL obtenido."

    # Ahora escribir la config final con SSL
    cat > "${NGINX_CONF}" <<EOF2
# Redirigir HTTP → HTTPS
server {
    listen 80;
    server_name ${DOMAIN} ${WWW_DOMAIN};
    return 301 https://\$host\$request_uri;
}

# Redirigir www → no-www (HTTPS)
server {
    listen 443 ssl http2;
    server_name ${WWW_DOMAIN};

    ssl_certificate     /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    include             /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam         /etc/letsencrypt/ssl-dhparams.pem;

    return 301 https://${DOMAIN}\$request_uri;
}

# Sitio principal (HTTPS)
server {
    listen 443 ssl http2;
    server_name ${DOMAIN};

    ssl_certificate     /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    include             /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam         /etc/letsencrypt/ssl-dhparams.pem;

    add_header X-Frame-Options           "SAMEORIGIN"            always;
    add_header X-XSS-Protection          "1; mode=block"         always;
    add_header X-Content-Type-Options    "nosniff"               always;
    add_header Referrer-Policy           "no-referrer-when-downgrade" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    client_max_body_size 20M;

    location /static/ {
        alias   ${PROJECT_DIR}/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias   ${PROJECT_DIR}/media/;
        expires 7d;
        add_header Cache-Control "public, no-transform";
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    location / {
        proxy_pass          http://127.0.0.1:8000;
        proxy_http_version  1.1;
        proxy_set_header    Host              \$host;
        proxy_set_header    X-Real-IP         \$remote_addr;
        proxy_set_header    X-Forwarded-For   \$proxy_add_x_forwarded_for;
        proxy_set_header    X-Forwarded-Proto \$scheme;
        proxy_read_timeout  60s;
        proxy_connect_timeout 60s;
    }

    access_log /var/log/nginx/cerveceros_access.log;
    error_log  /var/log/nginx/cerveceros_error.log;
}
EOF2

    nginx -t && systemctl reload nginx
    log "Nginx reconfigurado con SSL."
else
    warn "No se pudo obtener el certificado SSL automáticamente."
    warn "Verifica que el DNS de ${DOMAIN} apunte a la IP de este servidor."
    warn "Luego ejecuta manualmente:"
    warn "  sudo certbot --nginx -d ${DOMAIN} -d ${WWW_DOMAIN}"
fi

# ── Paso 12: Firewall ─────────────────────────────────────────────────────────
section "13 · Firewall (UFW)"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable
log "Firewall configurado."

# ── Paso 13: Fail2ban ─────────────────────────────────────────────────────────
section "14 · Fail2ban"
systemctl enable fail2ban
systemctl start fail2ban
log "Fail2ban activo."

# ── Paso 14: Permisos finales ─────────────────────────────────────────────────
section "15 · Permisos"
chown -R "${DEPLOY_USER}:www-data" "${PROJECT_DIR}"
# Directorios
find "${PROJECT_DIR}" -type d -exec chmod 755 {} \;
# Archivos del proyecto (excluir venv para no romper ejecutables)
find "${PROJECT_DIR}" -not -path "${VENV_DIR}/*" -type f -exec chmod 644 {} \;
# Restaurar permisos de ejecución del entorno virtual
find "${VENV_DIR}/bin" -type f -exec chmod 755 {} \;
find "${VENV_DIR}" -name '*.so' -type f -exec chmod 755 {} \;
# Archivos específicos del proyecto
chmod 600 "${PROJECT_DIR}/.env"
chmod +x "${PROJECT_DIR}/manage.py"
chmod -R 775 "${PROJECT_DIR}/media"
chmod -R 755 "${PROJECT_DIR}/staticfiles"
log "Permisos aplicados."

# ── Reinicio final ────────────────────────────────────────────────────────────
section "16 · Reinicio de servicios"
systemctl daemon-reload
systemctl restart gunicorn
systemctl restart nginx
log "Servicios reiniciados."

# ── Resumen ───────────────────────────────────────────────────────────────────
section "✅ Instalación completada"
echo -e "  ${BOLD}Sitio web   :${NC} https://${DOMAIN}"
echo -e "  ${BOLD}Panel admin :${NC} https://${DOMAIN}/panel/"
echo -e "  ${BOLD}Usuario     :${NC} ${ADMIN_USER}"
echo -e "  ${BOLD}Proyecto    :${NC} ${PROJECT_DIR}"
echo ""
echo -e "  ${BOLD}Logs Gunicorn:${NC}"
echo -e "    tail -f ${LOG_DIR}/error.log"
echo -e "    tail -f ${LOG_DIR}/access.log"
echo ""
echo -e "  ${BOLD}Logs Nginx:${NC}"
echo -e "    sudo tail -f /var/log/nginx/cerveceros_error.log"
echo ""
echo -e "  ${BOLD}Actualizar en el futuro:${NC}"
echo -e "    cd ${PROJECT_DIR} && source venv/bin/activate"
echo -e "    git pull origin main"
echo -e "    pip install -r requirements.txt"
echo -e "    python manage.py migrate"
echo -e "    python manage.py collectstatic --noinput"
echo -e "    sudo systemctl restart gunicorn"
echo ""

# Verificar estado de servicios
echo -e "${BOLD}Estado de servicios:${NC}"
systemctl is-active --quiet gunicorn && echo -e "  ${GREEN}✔ gunicorn${NC}" || echo -e "  ${RED}✘ gunicorn${NC}"
systemctl is-active --quiet nginx    && echo -e "  ${GREEN}✔ nginx${NC}"    || echo -e "  ${RED}✘ nginx${NC}"
systemctl is-active --quiet postgresql && echo -e "  ${GREEN}✔ postgresql${NC}" || echo -e "  ${RED}✘ postgresql${NC}"
echo ""
