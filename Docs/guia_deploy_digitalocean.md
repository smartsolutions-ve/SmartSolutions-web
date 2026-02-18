# Deploy de SmartSolutions VE en DigitalOcean

## Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Fase 1: Crear el Droplet](#fase-1-crear-el-droplet)
3. [Fase 2: Configuración Inicial del Servidor](#fase-2-configuración-inicial-del-servidor)
4. [Fase 3: Instalar Docker y Docker Compose](#fase-3-instalar-docker-y-docker-compose)
5. [Fase 4: Subir el Proyecto](#fase-4-subir-el-proyecto)
6. [Fase 5: Crear Dockerfile y docker-compose.yml](#fase-5-crear-dockerfile-y-docker-composeyml)
7. [Fase 6: Variables de Entorno](#fase-6-variables-de-entorno)
8. [Fase 7: Levantar la Aplicación](#fase-7-levantar-la-aplicación)
9. [Fase 8: Configurar Nginx](#fase-8-configurar-nginx)
10. [Fase 9: SSL con Let's Encrypt](#fase-9-ssl-con-lets-encrypt)
11. [Fase 10: Dominio DNS](#fase-10-dominio-dns)
12. [Fase 11: Configuración Post-Deploy](#fase-11-configuración-post-deploy)
13. [Mantenimiento](#mantenimiento)
14. [Referencia Rápida](#referencia-rápida)
15. [Troubleshooting](#troubleshooting)

---

## Requisitos Previos

- Cuenta en DigitalOcean
- Dominio registrado (ej: `smartsolutions.com.ve`)
- Cuenta en [Resend.com](https://resend.com) para emails (plan gratuito)
- SSH en tu computadora (Linux/Mac nativo)

**Costo mensual estimado:**
- Droplet $6/mes (1GB RAM, 1 CPU, 25GB SSD)
- SSL: gratis (Let's Encrypt)

---

## Fase 1: Crear el Droplet

1. Inicia sesión en https://cloud.digitalocean.com
2. **Create → Droplets**
3. Configuración:
   ```
   Region:      New York (mejor latencia para Venezuela)
   Image:       Ubuntu 24.04 LTS x64
   Plan:        Basic → Regular CPU → $6/mo
   Auth:        SSH Key (recomendado) o Password
   Hostname:    smartsolutions-prod
   ```

4. Si usas SSH Key, genérala en tu computadora:
   ```bash
   ssh-keygen -t ed25519 -C "tu@email.com"
   cat ~/.ssh/id_ed25519.pub
   # Pega el resultado en DigitalOcean → Add SSH Key
   ```

5. **Create Droplet** → copia la IP pública (ej: `164.92.XXX.XXX`)

---

## Fase 2: Configuración Inicial del Servidor

### 2.1 Conectarte por SSH

```bash
# Con SSH key:
ssh -i ~/.ssh/id_ed25519 root@TU_IP

# Con contraseña:
ssh root@TU_IP
# Primera vez: acepta con "yes"
```

### 2.2 Actualizar el sistema

```bash
apt update && apt upgrade -y
```

### 2.3 Crear usuario deploy (no usar root)

```bash
adduser deploy
# Pon una contraseña segura y guárdala

usermod -aG sudo deploy
su - deploy
```

### 2.4 Configurar firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status
```

---

## Fase 3: Instalar Docker y Docker Compose

```bash
# Dependencias
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# GPG key de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Repositorio Docker
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Verificar
docker --version

# Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

---

## Fase 4: Subir el Proyecto

El proyecto está en GitHub en `https://github.com/smartsolutions-ve/SmartSolutions-web`.
No se usa ZIP — el servidor clona el repositorio directamente.

### 4.1 Desde tu computadora: hacer push

```bash
cd "/home/sabh/Documentos/Smart Solutions/smartsolutions"

# Verificar que todo esté commiteado
git status

# Hacer push al repositorio
git push origin main
```

### 4.2 En el servidor: clonar el repositorio

```bash
# Instalar git (si no está)
sudo apt install -y git

# Clonar el repositorio en el home de deploy
cd ~
git clone https://github.com/smartsolutions-ve/SmartSolutions-web.git smartsolutions

# Verificar estructura
ls ~/smartsolutions/
# Debes ver: apps/ config/ manage.py requirements.txt static/ templates/ Docs/ ...

# Crear directorios que no van en Git (.gitignore los excluye)
mkdir -p ~/smartsolutions/postgres-data
mkdir -p ~/smartsolutions/nginx/conf.d
mkdir -p ~/smartsolutions/certbot/{conf,www}
mkdir -p ~/smartsolutions/staticfiles
mkdir -p ~/smartsolutions/media
```

**Nota:** El `.gitignore` ya excluye correctamente `venv/`, `.env`, `db.sqlite3`, `media/` y `staticfiles/`. Nunca se subirán datos sensibles al repositorio.

---

## Fase 5: Crear Dockerfile y docker-compose.yml

### 5.1 Dockerfile

```bash
nano ~/smartsolutions/Dockerfile
```

```dockerfile
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dependencias del sistema (psycopg2 requiere libpq-dev)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

Guarda: `Ctrl+O`, Enter, `Ctrl+X`

### 5.2 docker-compose.yml

```bash
nano ~/docker-compose.yml
```

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    container_name: smartsolutions_db
    restart: always
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./smartsolutions/postgres-data:/var/lib/postgresql/data
    networks:
      - smartsolutions_network

  web:
    build: ./smartsolutions
    container_name: smartsolutions_web
    restart: always
    env_file:
      - .env
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - db
    networks:
      - smartsolutions_network
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3"

  nginx:
    image: nginx:alpine
    container_name: smartsolutions_nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./smartsolutions/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./smartsolutions/nginx/conf.d:/etc/nginx/conf.d:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
      - ./smartsolutions/certbot/conf:/etc/letsencrypt:ro
      - ./smartsolutions/certbot/www:/var/www/certbot:ro
    depends_on:
      - web
    networks:
      - smartsolutions_network

volumes:
  static_volume:
  media_volume:

networks:
  smartsolutions_network:
    driver: bridge
```

Guarda: `Ctrl+O`, Enter, `Ctrl+X`

**Nota:** El `docker-compose.yml` va en `~/` (un nivel arriba de `smartsolutions/`) para que el contexto de build apunte correctamente a `./smartsolutions`.

---

## Fase 6: Variables de Entorno

```bash
nano ~/.env
```

```bash
# Django
SECRET_KEY=CAMBIA_ESTO_genera_una_clave_de_50_caracteres_random
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,TU_IP_PUBLICA

# Base de datos (el host "db" es el nombre del servicio en docker-compose)
DB_NAME=smartsolutions
DB_USER=smartsolutions
DB_PASSWORD=CAMBIA_ESTO_contraseña_segura_para_postgres
DB_HOST=db
DB_PORT=5432

# Email (Resend — https://resend.com)
RESEND_API_KEY=re_tu_api_key_aqui
DEFAULT_FROM_EMAIL=noreply@tu-dominio.com
CONTACT_EMAIL=tu@email.com

# URL del sitio
SITE_URL=https://tu-dominio.com
```

Guarda: `Ctrl+O`, Enter, `Ctrl+X`

**Generar SECRET_KEY segura:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Proteger el archivo .env:**
```bash
chmod 600 ~/.env
```

---

## Fase 7: Levantar la Aplicación

### 7.1 Construir la imagen Django

```bash
cd ~
docker-compose build web

# Si hay errores de build, ver detalles:
docker-compose build web --no-cache
```

### 7.2 Levantar base de datos primero

```bash
docker-compose up -d db

# Esperar ~5 segundos a que PostgreSQL inicialice
sleep 5

# Verificar que está corriendo
docker-compose ps
```

### 7.3 Levantar la aplicación completa

```bash
docker-compose up -d

# Ver logs para verificar que todo está OK
docker-compose logs -f web
# Si ves "Booting worker" → Django está corriendo correctamente
# Presiona Ctrl+C para salir de los logs
```

### 7.4 Crear superusuario de Django

```bash
docker-compose exec web python manage.py createsuperuser
# Username: admin
# Email: tu@email.com
# Password: (elige una contraseña segura)
```

### 7.5 Crear la ConfiguracionSitio inicial

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.core.models import ConfiguracionSitio
ConfiguracionSitio.objects.create(
    nombre_empresa="SmartSolutions VE",
    slogan="Transformamos el Caos en Claridad",
    descripcion_corta="Consultoría empresarial especializada en transformación organizacional para PYMEs venezolanas.",
    email="contacto@smartsolutions.com.ve",
    telefono="+58 412 169 1851",
    whatsapp="+58 412 169 1851",
    ciudad="Valencia",
    pais="Venezuela",
)
exit()
```

---

## Fase 8: Configurar Nginx

### 8.1 nginx.conf principal

```bash
nano ~/smartsolutions/nginx/nginx.conf
```

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    client_max_body_size 20M;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml image/svg+xml;

    include /etc/nginx/conf.d/*.conf;
}
```

### 8.2 Configuración del sitio (sin SSL por ahora)

```bash
nano ~/smartsolutions/nginx/conf.d/smartsolutions.conf
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    # Para Let's Encrypt (obtener el certificado)
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Temporal: servir directo hasta tener SSL
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /app/media/;
        expires 7d;
    }
}
```

### 8.3 Reiniciar Nginx

```bash
docker-compose restart nginx
docker-compose logs nginx
# No debe haber errores
```

### 8.4 Verificar que el sitio responde

```bash
# Desde tu computadora local:
curl -I http://TU_IP_PUBLICA
# Debe responder HTTP/1.1 200 OK
```

---

## Fase 9: SSL con Let's Encrypt

**Prerequisito:** El dominio debe apuntar a la IP del servidor (ver Fase 10). Si el dominio aún no está configurado, salta a Fase 10 y vuelve aquí.

### 9.1 Obtener certificado SSL

```bash
# Cambia tu-dominio.com y tu@email.com
docker run -it --rm \
  -v ~/smartsolutions/certbot/conf:/etc/letsencrypt \
  -v ~/smartsolutions/certbot/www:/var/www/certbot \
  certbot/certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email tu@email.com \
  --agree-tos \
  --no-eff-email \
  -d tu-dominio.com \
  -d www.tu-dominio.com

# Si sale "Successfully received certificate" → listo
```

### 9.2 Actualizar configuración Nginx con HTTPS

```bash
nano ~/smartsolutions/nginx/conf.d/smartsolutions.conf
```

Reemplaza TODO el contenido con:

```nginx
# HTTP → redirigir a HTTPS
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Django app
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Archivos estáticos (CSS, JS, imágenes)
    # WhiteNoise los maneja desde Django, pero Nginx es más eficiente
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Archivos subidos (fotos de testimonios, casos de éxito)
    location /media/ {
        alias /app/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    client_max_body_size 20M;
}
```

```bash
docker-compose restart nginx
docker-compose logs nginx
```

### 9.3 Renovación automática de SSL

```bash
nano ~/renew-ssl.sh
```

```bash
#!/bin/bash
cd /home/deploy

docker run --rm \
  -v $PWD/smartsolutions/certbot/conf:/etc/letsencrypt \
  -v $PWD/smartsolutions/certbot/www:/var/www/certbot \
  certbot/certbot renew

docker-compose restart nginx
```

```bash
chmod +x ~/renew-ssl.sh

# Cron: renovar cada día a las 3am
crontab -e
# Agregar al final:
0 3 * * * /home/deploy/renew-ssl.sh >> /home/deploy/ssl-renew.log 2>&1
```

---

## Fase 10: Dominio DNS

Ve al panel de tu proveedor de dominio y crea:

```
Tipo: A     Nombre: @    Valor: TU_IP_PUBLICA    TTL: 3600
Tipo: A     Nombre: www  Valor: TU_IP_PUBLICA    TTL: 3600
```

Verificar propagación (puede tardar 5 min - 48 horas):
```bash
nslookup tu-dominio.com
# Debe mostrar TU_IP_PUBLICA
```

---

## Fase 11: Configuración Post-Deploy

### 11.1 Completar ConfiguracionSitio desde admin

Accede a `https://tu-dominio.com/admin/` y completa todos los campos de **Config. del Sitio**:
- Nombre empresa, slogan, descripción
- Redes sociales (LinkedIn, Instagram)
- Métricas del Hero (clientes, proyectos, años)
- Texto de los botones CTA

### 11.2 Agregar contenido inicial

Desde el admin, crea:
- Al menos 3 **Servicios** (con título, descripción, ícono Font Awesome)
- Al menos 2 **Testimonios** (con foto, nombre, cargo, empresa, texto)
- Al menos 1 **Caso de Éxito** (con título, métricas, imagen)

### 11.3 Verificar el formulario de contacto

- Llena el formulario en la landing
- Verifica que llega el email de notificación
- Verifica que el lead aparece en `/admin/landing/lead/`

---

## Mantenimiento

### Backup automático de base de datos

```bash
nano ~/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR=/home/deploy/backups
mkdir -p $BACKUP_DIR
DATE=$(date +%Y%m%d_%H%M%S)

cd /home/deploy
docker-compose exec -T db pg_dump -U smartsolutions smartsolutions > $BACKUP_DIR/smartsolutions_$DATE.sql
gzip $BACKUP_DIR/smartsolutions_$DATE.sql

# Mantener solo los últimos 7 backups
ls -t $BACKUP_DIR/*.sql.gz | tail -n +8 | xargs rm -f

echo "Backup OK: smartsolutions_$DATE.sql.gz"
```

```bash
chmod +x ~/backup-db.sh

# Cron: backup diario a las 2am
crontab -e
# Agregar:
0 2 * * * /home/deploy/backup-db.sh >> /home/deploy/backup.log 2>&1
```

### Restaurar un backup

```bash
gunzip ~/backups/smartsolutions_FECHA.sql.gz
cd ~
docker-compose exec -T db psql -U smartsolutions smartsolutions < ~/backups/smartsolutions_FECHA.sql
```

---

## Referencia Rápida

```bash
# Acceder al servidor
ssh deploy@TU_IP

# Ver estado de servicios
cd ~ && docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f web       # Django
docker-compose logs -f nginx     # Nginx
docker-compose logs -f db        # PostgreSQL

# Reiniciar servicios
docker-compose restart web
docker-compose restart nginx

# Comandos Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py shell

# Acceder a PostgreSQL
docker-compose exec db psql -U smartsolutions -d smartsolutions

# Ver uso de recursos
docker stats

# Limpiar espacio en disco
docker system prune -a
```

### Deploy de actualizaciones

```bash
# 1. Desde tu computadora local: commit y push
cd "/home/sabh/Documentos/Smart Solutions/smartsolutions"
git add -p                          # Revisar cambios antes de agregar
git commit -m "descripción del cambio"
git push origin main

# 2. En el servidor: bajar cambios y reconstruir
ssh deploy@TU_IP
cd ~
git -C smartsolutions pull origin main

# 3. Reconstruir imagen y reiniciar Django
docker-compose build web
docker-compose up -d --force-recreate web

# 4. Verificar
docker-compose logs -f web
```

El flujo completo tarda menos de 2 minutos.

---

## Troubleshooting

### Error: "Connection refused" al visitar el sitio

```bash
docker-compose ps                  # ¿Están corriendo los contenedores?
docker-compose logs nginx          # ¿Nginx tiene errores?
docker-compose logs web            # ¿Django arrancó bien?
```

Si `web` no está corriendo: `docker-compose up -d web`

---

### Error: 502 Bad Gateway

Nginx no puede conectar con Django.

```bash
# Verificar que Django responde dentro del contenedor
docker-compose exec nginx wget -q -O- http://web:8000 | head -20

# Si no responde:
docker-compose restart web
docker-compose logs -f web
```

---

### Error: CSS/JS no se ven (archivos estáticos)

```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
docker-compose exec web ls -la /app/staticfiles/
```

---

### Error: "CSRF verification failed" en formulario

Verifica en `.env`:
```bash
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,TU_IP
```

Reinicia: `docker-compose restart web`

---

### Error: Loop de redirección HTTPS (ERR_TOO_MANY_REDIRECTS)

Esto pasa si falta `SECURE_PROXY_SSL_HEADER` en settings.py. Ya está configurado en la versión actual del proyecto. Verifica que `config/settings.py` tenga:

```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

---

### Espacio en disco lleno

```bash
df -h                          # Ver uso de disco
docker system df               # Ver tamaño de imágenes Docker
docker system prune -a         # Limpiar imágenes no usadas
sudo journalctl --vacuum-time=7d  # Limpiar logs del sistema
```

---

## Checklist Final

- [ ] El sitio carga en `https://tu-dominio.com`
- [ ] Redirige HTTP → HTTPS automáticamente
- [ ] CSS/JS se ven correctamente (sin errores en consola)
- [ ] Puedes acceder al admin en `/admin/`
- [ ] La ConfiguracionSitio está completada
- [ ] Hay contenido en Servicios, Testimonios, Casos de Éxito
- [ ] El formulario de contacto envía emails
- [ ] El certificado SSL está activo (candado en navegador)
- [ ] Backup automático configurado (cron)
- [ ] Renovación SSL automática configurada (cron)
