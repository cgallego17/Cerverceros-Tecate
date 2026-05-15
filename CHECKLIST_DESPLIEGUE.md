# ✅ Checklist de Despliegue - Cerveceros de Tecate

## 📦 Archivos de Configuración

- [x] `requirements.txt` - Dependencias completas
- [x] `.env.example` - Plantilla de variables de entorno
- [x] `gunicorn_config.py` - Configuración de Gunicorn
- [x] `nginx_cerveceros.conf` - Configuración de Nginx
- [x] `.gitignore` - Archivos a ignorar en Git
- [x] `DESPLIEGUE_DIGITAL_OCEAN.md` - Guía paso a paso

## ⚙️ Configuración de Django

- [x] `settings.py` configurado con variables de entorno
- [x] `DEBUG` configurable desde .env
- [x] `SECRET_KEY` configurable desde .env
- [x] `ALLOWED_HOSTS` configurable desde .env
- [x] Base de datos PostgreSQL/SQLite configurable
- [x] WhiteNoise para archivos estáticos
- [x] Configuración de seguridad SSL
- [x] Middleware de internacionalización (i18n)

## 🌐 Multiidioma

- [x] i18n_patterns configurado en URLs
- [x] Archivos de traducción compilados (ES/EN)
- [x] Botones de cambio de idioma en sitio público
- [x] Botones de cambio de idioma en panel
- [x] LocaleMiddleware configurado

## 📊 Base de Datos

- [x] Modelos creados y migrados
- [x] Admin configurado con vistas previas
- [x] Comando de contenido de prueba disponible

## 🎨 Frontend

- [x] Templates con i18n
- [x] Archivos estáticos organizados
- [x] Imágenes placeholder configuradas
- [x] Responsive design

## 🔐 Panel de Administración

- [x] Panel personalizado funcional
- [x] Sistema de autenticación
- [x] CRUD completo para todos los modelos
- [x] Multiidioma en panel

## 📝 Antes de Desplegar

1. [ ] Crear repositorio en GitHub
2. [ ] Subir código a GitHub
3. [ ] Crear droplet en Digital Ocean (Ubuntu 22.04 LTS)
4. [ ] Configurar dominio (opcional)

## 🚀 Pasos de Despliegue

Sigue la guía completa en: **DESPLIEGUE_DIGITAL_OCEAN.md**

### Resumen Rápido:

1. **Conectar al servidor**
   ```bash
   ssh root@tu-ip-del-droplet
   ```

2. **Instalar dependencias del sistema**
   ```bash
   apt update && apt upgrade -y
   apt install -y python3.11 python3.11-venv python3-pip nginx postgresql
   ```

3. **Configurar PostgreSQL**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE cerveceros_db;
   CREATE USER cerveceros_user WITH PASSWORD 'tu-password';
   GRANT ALL PRIVILEGES ON DATABASE cerveceros_db TO cerveceros_user;
   ```

4. **Clonar proyecto**
   ```bash
   git clone tu-repositorio.git cerveceros_tecate
   cd cerveceros_tecate
   ```

5. **Configurar entorno virtual**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configurar .env**
   ```bash
   cp .env.example .env
   nano .env
   # Editar con tus valores
   ```

7. **Preparar Django**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   python manage.py compilemessages
   ```

8. **Configurar Gunicorn**
   ```bash
   sudo cp gunicorn.service /etc/systemd/system/
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```

9. **Configurar Nginx**
   ```bash
   sudo cp nginx_cerveceros.conf /etc/nginx/sites-available/cerveceros
   sudo ln -s /etc/nginx/sites-available/cerveceros /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

10. **Configurar SSL (opcional)**
    ```bash
    sudo certbot --nginx -d tu-dominio.com
    ```

## ✅ Verificación Post-Despliegue

- [ ] Sitio accesible desde el navegador
- [ ] Panel admin funcional
- [ ] Cambio de idioma funcionando
- [ ] Subida de imágenes funcional
- [ ] Archivos estáticos cargando
- [ ] SSL configurado (si aplica)

## 🔧 Comandos Útiles

### Ver logs
```bash
tail -f /var/log/gunicorn/error.log
tail -f /var/log/nginx/cerveceros_error.log
```

### Reiniciar servicios
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Actualizar código
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages
sudo systemctl restart gunicorn
```

---

## 🎯 ¿Listo para Desplegar?

**SÍ** - Todo está configurado y listo. Sigue la guía en `DESPLIEGUE_DIGITAL_OCEAN.md`

**Proyecto:** Cerveceros de Tecate
**Versión:** 1.0.0
**Fecha:** Mayo 2026

🍺⚾ ¡Vamos Cerveceros!
