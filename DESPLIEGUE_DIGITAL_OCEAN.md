# 🚀 Guía de Despliegue - Cerveceros de Tecate
## Digital Ocean Ubuntu Server

Esta guía te llevará paso a paso para desplegar el proyecto en un droplet de Digital Ocean.

---

## 📋 Requisitos Previos

- Droplet de Digital Ocean con Ubuntu 22.04 LTS
- Dominio apuntando a la IP del droplet (opcional pero recomendado)
- Acceso SSH al servidor

---

## 1️⃣ Configuración Inicial del Servidor

### Conectarse al servidor
```bash
ssh root@tu-ip-del-droplet
```

### Actualizar el sistema
```bash
apt update && apt upgrade -y
```

### Crear usuario para deployment
```bash
adduser deploy
usermod -aG sudo deploy
su - deploy
```

---

## 2️⃣ Instalar Dependencias del Sistema

### Instalar Python y herramientas
```bash
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y nginx postgresql postgresql-contrib
sudo apt install -y git curl
```

### Instalar dependencias para Pillow (manejo de imágenes)
```bash
sudo apt install -y libjpeg-dev zlib1g-dev libpq-dev
```

---

## 3️⃣ Configurar PostgreSQL

### Crear base de datos y usuario
```bash
sudo -u postgres psql
```

Dentro de PostgreSQL:
```sql
CREATE DATABASE cerveceros_db;
CREATE USER cerveceros_user WITH PASSWORD 'tu-password-seguro-aqui';
ALTER ROLE cerveceros_user SET client_encoding TO 'utf8';
ALTER ROLE cerveceros_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cerveceros_user SET timezone TO 'America/Tijuana';
GRANT ALL PRIVILEGES ON DATABASE cerveceros_db TO cerveceros_user;
\q
```

---

## 4️⃣ Clonar y Configurar el Proyecto

### Clonar el repositorio
```bash
cd /home/deploy
git clone https://github.com/tu-usuario/cerveceros-tecate.git cerveceros_tecate
cd cerveceros_tecate
```

### Crear entorno virtual
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5️⃣ Configurar Variables de Entorno

### Crear archivo .env
```bash
nano .env
```

Agregar el siguiente contenido (ajusta los valores):
```env
# Django Settings
SECRET_KEY=genera-una-clave-secreta-segura-aqui
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,tu-ip-del-droplet

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=cerveceros_db
DB_USER=cerveceros_user
DB_PASSWORD=tu-password-seguro-aqui
DB_HOST=localhost
DB_PORT=5432
```

**Generar SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 6️⃣ Preparar Django

### Ejecutar migraciones
```bash
python manage.py migrate
```

### Crear superusuario
```bash
python manage.py createsuperuser
```

### Crear contenido de prueba
```bash
python manage.py crear_contenido_prueba
```

### Recolectar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

### Crear carpetas para media
```bash
mkdir -p media/{jugadores,equipos,noticias,hero,patrocinadores,productos,news,instagram}
```

---

## 7️⃣ Configurar Gunicorn

### Crear directorios para logs
```bash
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R deploy:www-data /var/log/gunicorn
sudo chown -R deploy:www-data /var/run/gunicorn
```

### Crear servicio systemd para Gunicorn
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Contenido del archivo:
```ini
[Unit]
Description=Gunicorn daemon for Cerveceros de Tecate
After=network.target

[Service]
User=deploy
Group=www-data
WorkingDirectory=/home/deploy/cerveceros_tecate
Environment="PATH=/home/deploy/cerveceros_tecate/venv/bin"
ExecStart=/home/deploy/cerveceros_tecate/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          --access-logfile /var/log/gunicorn/access.log \
          --error-logfile /var/log/gunicorn/error.log \
          cerveceros_tecate.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Iniciar y habilitar Gunicorn
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

---

## 8️⃣ Configurar Nginx

### Copiar configuración de Nginx
```bash
sudo cp nginx_cerveceros.conf /etc/nginx/sites-available/cerveceros
```

### Editar la configuración
```bash
sudo nano /etc/nginx/sites-available/cerveceros
```

Reemplazar:
- `tu-dominio.com` con tu dominio real
- `/home/deploy/cerveceros_tecate` con la ruta correcta si es diferente

### Activar el sitio
```bash
sudo ln -s /etc/nginx/sites-available/cerveceros /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Opcional: remover sitio por defecto
```

### Verificar configuración
```bash
sudo nginx -t
```

### Reiniciar Nginx
```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

## 9️⃣ Configurar Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

---

## 🔟 Configurar SSL con Let's Encrypt (Opcional pero Recomendado)

### Instalar Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Obtener certificado SSL
```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Sigue las instrucciones en pantalla.

### Renovación automática
Certbot configura automáticamente la renovación. Verifica:
```bash
sudo certbot renew --dry-run
```

---

## 🔄 Comandos Útiles para Mantenimiento

### Reiniciar servicios
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Ver logs
```bash
# Logs de Gunicorn
tail -f /var/log/gunicorn/error.log
tail -f /var/log/gunicorn/access.log

# Logs de Nginx
sudo tail -f /var/log/nginx/cerveceros_error.log
sudo tail -f /var/log/nginx/cerveceros_access.log
```

### Actualizar el proyecto
```bash
cd /home/deploy/cerveceros_tecate
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Backup de la base de datos
```bash
pg_dump -U cerveceros_user cerveceros_db > backup_$(date +%Y%m%d).sql
```

### Restaurar base de datos
```bash
psql -U cerveceros_user cerveceros_db < backup_20260514.sql
```

---

## 🎯 Verificación Final

1. **Accede a tu sitio:** http://tu-dominio.com
2. **Panel de administración:** http://tu-dominio.com/admin/
3. **Verifica que las imágenes se suban correctamente**
4. **Verifica que los archivos estáticos se carguen**

---

## 🐛 Solución de Problemas

### Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté corriendo
sudo systemctl status gunicorn

# Revisar logs
tail -f /var/log/gunicorn/error.log
```

### Archivos estáticos no se cargan
```bash
# Recolectar archivos estáticos nuevamente
python manage.py collectstatic --noinput

# Verificar permisos
sudo chown -R deploy:www-data /home/deploy/cerveceros_tecate/staticfiles
sudo chmod -R 755 /home/deploy/cerveceros_tecate/staticfiles
```

### No se pueden subir imágenes
```bash
# Verificar permisos de la carpeta media
sudo chown -R deploy:www-data /home/deploy/cerveceros_tecate/media
sudo chmod -R 775 /home/deploy/cerveceros_tecate/media
```

### Error de base de datos
```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql

# Verificar conexión
psql -U cerveceros_user -d cerveceros_db -h localhost
```

---

## 📊 Monitoreo

### Instalar herramientas de monitoreo (opcional)
```bash
sudo apt install -y htop
```

### Ver uso de recursos
```bash
htop
```

---

## 🔐 Seguridad Adicional

### Cambiar puerto SSH (opcional)
```bash
sudo nano /etc/ssh/sshd_config
# Cambiar Port 22 a otro puerto
sudo systemctl restart sshd
```

### Configurar fail2ban
```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## ✅ Checklist de Despliegue

- [ ] Servidor actualizado
- [ ] PostgreSQL instalado y configurado
- [ ] Usuario deploy creado
- [ ] Proyecto clonado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Archivo .env configurado
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Archivos estáticos recolectados
- [ ] Gunicorn configurado y corriendo
- [ ] Nginx configurado y corriendo
- [ ] Firewall configurado
- [ ] SSL configurado (opcional)
- [ ] Sitio accesible desde el navegador
- [ ] Panel admin funcional
- [ ] Subida de imágenes funcional

---

## 📞 Soporte

Si encuentras problemas, revisa:
1. Logs de Gunicorn: `/var/log/gunicorn/error.log`
2. Logs de Nginx: `/var/log/nginx/cerveceros_error.log`
3. Logs de Django: Verifica la configuración de logging en settings.py

---

¡Listo! Tu sitio de Cerveceros de Tecate está desplegado en Digital Ocean. 🍺⚾
