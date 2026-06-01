#!/usr/bin/env bash
# =============================================================================
#  Cerveceros de Tecate — Script de Actualización
#  Uso: sudo bash update.sh
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
DEPLOY_USER="deploy"
PROJECT_DIR="/home/${DEPLOY_USER}/cerveceros_tecate"
VENV_DIR="${PROJECT_DIR}/venv"
PYTHON_BIN="${VENV_DIR}/bin/python"
PIP_BIN="${VENV_DIR}/bin/pip"

# ── Verificaciones previas ────────────────────────────────────────────────────
[[ $EUID -ne 0 ]] && die "Ejecuta el script como root: sudo bash update.sh"
[[ ! -d "${PROJECT_DIR}" ]] && die "El proyecto no existe en ${PROJECT_DIR}"

section "Cerveceros de Tecate — Actualización"
echo -e "  Proyecto: ${BOLD}${PROJECT_DIR}${NC}"
echo ""

# ── Paso 1: Hacer backup de la base de datos ─────────────────────────────────
section "1 · Backup de base de datos"
BACKUP_DIR="${PROJECT_DIR}/backups"
BACKUP_FILE="${BACKUP_DIR}/db_backup_$(date +%Y%m%d_%H%M%S).sql"

sudo -u "${DEPLOY_USER}" mkdir -p "${BACKUP_DIR}"

info "Creando backup en ${BACKUP_FILE}..."
sudo -u postgres pg_dump cerveceros_db > "${BACKUP_FILE}"
sudo chown "${DEPLOY_USER}:${DEPLOY_USER}" "${BACKUP_FILE}"
log "Backup creado exitosamente."

# ── Paso 2: Detener Gunicorn ─────────────────────────────────────────────────
section "2 · Detener Gunicorn"
systemctl stop gunicorn
log "Gunicorn detenido."

# ── Paso 3: Actualizar código desde Git ──────────────────────────────────────
section "3 · Actualizar código"
cd "${PROJECT_DIR}"
info "Obteniendo últimos cambios de Git..."
sudo -u "${DEPLOY_USER}" git fetch origin
sudo -u "${DEPLOY_USER}" git pull origin main
log "Código actualizado."

# ── Paso 4: Actualizar dependencias ──────────────────────────────────────────
section "4 · Actualizar dependencias Python"
info "Actualizando pip..."
sudo -u "${DEPLOY_USER}" "${PIP_BIN}" install --upgrade pip -q

info "Instalando/actualizando dependencias..."
sudo -u "${DEPLOY_USER}" "${PIP_BIN}" install -r "${PROJECT_DIR}/requirements.txt" -q
log "Dependencias actualizadas."

# ── Paso 5: Ejecutar migraciones ─────────────────────────────────────────────
section "5 · Migraciones de base de datos"
info "Ejecutando migraciones..."
sudo -u "${DEPLOY_USER}" "${PYTHON_BIN}" manage.py migrate --noinput
log "Migraciones aplicadas."

# ── Paso 6: Recolectar archivos estáticos ────────────────────────────────────
section "6 · Archivos estáticos"
info "Recolectando archivos estáticos..."
sudo -u "${DEPLOY_USER}" "${PYTHON_BIN}" manage.py collectstatic --noinput --clear -v 0
log "Archivos estáticos recolectados."

# ── Paso 7: Compilar traducciones ────────────────────────────────────────────
section "7 · Traducciones"
info "Compilando mensajes de traducción..."
sudo -u "${DEPLOY_USER}" "${PYTHON_BIN}" manage.py compilemessages 2>/dev/null || warn "No se encontraron archivos de traducción."
log "Traducciones compiladas."

# ── Paso 8: Ajustar permisos ──────────────────────────────────────────────────
section "8 · Permisos"
info "Ajustando permisos..."

# Permisos del directorio home
chmod 755 /home/deploy

# Permisos del proyecto
chown -R "${DEPLOY_USER}:www-data" "${PROJECT_DIR}"

# Directorios
find "${PROJECT_DIR}" -type d -exec chmod 755 {} \;

# Archivos (excluir venv)
find "${PROJECT_DIR}" -not -path "${VENV_DIR}/*" -type f -exec chmod 644 {} \;

# Restaurar permisos de ejecución del venv
find "${VENV_DIR}/bin" -type f -exec chmod 755 {} \;
find "${VENV_DIR}" -name '*.so' -type f -exec chmod 755 {} \;

# Archivos específicos
chmod 600 "${PROJECT_DIR}/.env"
chmod +x "${PROJECT_DIR}/manage.py"
chmod -R 775 "${PROJECT_DIR}/media"
chmod -R 755 "${PROJECT_DIR}/staticfiles"

log "Permisos aplicados."

# ── Paso 9: Reiniciar servicios ──────────────────────────────────────────────
section "9 · Reiniciar servicios"
systemctl daemon-reload
systemctl start gunicorn
systemctl restart nginx
log "Servicios reiniciados."

# ── Paso 10: Verificar estado ────────────────────────────────────────────────
section "10 · Verificación"
sleep 2

echo -e "${BOLD}Estado de servicios:${NC}"
systemctl is-active --quiet gunicorn && echo -e "  ${GREEN}✔ gunicorn${NC}" || echo -e "  ${RED}✘ gunicorn${NC}"
systemctl is-active --quiet nginx    && echo -e "  ${GREEN}✔ nginx${NC}"    || echo -e "  ${RED}✘ nginx${NC}"
echo ""

# ── Resumen ───────────────────────────────────────────────────────────────────
section "✅ Actualización completada"
echo -e "  ${BOLD}Sitio web   :${NC} https://cervecerosdetecate.com"
echo -e "  ${BOLD}Panel admin :${NC} https://cervecerosdetecate.com/panel/"
echo -e "  ${BOLD}Backup DB   :${NC} ${BACKUP_FILE}"
echo ""
echo -e "  ${BOLD}Ver logs:${NC}"
echo -e "    sudo tail -f /var/log/gunicorn/error.log"
echo -e "    sudo tail -f /var/log/nginx/cerveceros_error.log"
echo ""
echo -e "  ${BOLD}Restaurar backup (si es necesario):${NC}"
echo -e "    sudo -u postgres psql cerveceros_db < ${BACKUP_FILE}"
echo ""

log "¡Actualización exitosa! 🍺⚾"
