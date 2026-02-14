# Documentación Completa de Tecnologías para Deploy de SmartSolutions VE

> **Objetivo:** Entender cada tecnología involucrada en el despliegue de una aplicación Django en un servidor DigitalOcean, al nivel necesario para completar todo el procedimiento con confianza.

---

## Tabla de Contenidos

1. [SSH (Secure Shell)](#1-ssh-secure-shell)
2. [Linux / Ubuntu Server](#2-linux--ubuntu-server)
3. [UFW (Firewall)](#3-ufw-uncomplicated-firewall)
4. [Docker](#4-docker)
5. [Docker Compose](#5-docker-compose)
6. [PostgreSQL](#6-postgresql)
7. [Django en Producción](#7-django-en-producción)
8. [Gunicorn](#8-gunicorn)
9. [Nginx](#9-nginx)
10. [SSL/TLS y Let's Encrypt](#10-ssltls-y-lets-encrypt)
11. [DNS (Sistema de Nombres de Dominio)](#11-dns-sistema-de-nombres-de-dominio)
12. [DigitalOcean (Infraestructura Cloud)](#12-digitalocean-infraestructura-cloud)
13. [Cron (Tareas Programadas)](#13-cron-tareas-programadas)
14. [Variables de Entorno y Archivos .env](#14-variables-de-entorno-y-archivos-env)
15. [Cómo Encajan Todas las Piezas](#15-cómo-encajan-todas-las-piezas)

---

## 1. SSH (Secure Shell)

### Qué es

SSH es un protocolo de red que te permite conectarte de forma segura a un servidor remoto a través de una terminal. Toda la comunicación viaja encriptada, lo que significa que nadie puede interceptar tus contraseñas o comandos.

Cuando haces deploy, SSH es tu única forma de interactuar con el servidor. No hay interfaz gráfica — todo se hace escribiendo comandos en una terminal.

### Cómo funciona la conexión

Cuando escribes `ssh deploy@164.92.100.50`, sucede lo siguiente:

1. Tu computadora contacta al servidor en el puerto 22 (el puerto estándar de SSH).
2. El servidor presenta su "huella digital" (fingerprint). La primera vez que te conectas, tu terminal te pregunta si confías en ese servidor — escribes `yes` y esa huella se guarda localmente.
3. Se establece un canal encriptado.
4. Te autenticas con contraseña o con llave SSH.
5. Obtienes una terminal remota donde cada comando se ejecuta directamente en el servidor.

### Autenticación por contraseña vs. llaves SSH

**Autenticación por contraseña** es la forma más simple: el servidor te pide una contraseña y la verificas. El problema es que las contraseñas pueden ser adivinadas por fuerza bruta.

**Autenticación por llaves SSH** es mucho más segura y funciona así:

- Generas un par de llaves en tu computadora: una **llave privada** (se queda en tu máquina, nunca la compartes) y una **llave pública** (se copia al servidor).
- Cuando te conectas, el servidor envía un desafío criptográfico que solo puede resolver quien tenga la llave privada.
- No se transmite ninguna contraseña por la red.

```bash
# Generar un par de llaves (se ejecuta en TU computadora, no en el servidor)
ssh-keygen -t ed25519 -C "simon@smartsolutions.com"
```

Esto crea dos archivos:
- `~/.ssh/id_ed25519` → llave privada (NUNCA la compartas)
- `~/.ssh/id_ed25519.pub` → llave pública (esta la copias al servidor)

El flag `-t ed25519` indica el algoritmo criptográfico. Ed25519 es moderno, rápido y más seguro que el antiguo RSA.

### SCP: Copiar archivos por SSH

SCP (Secure Copy Protocol) usa el mismo canal encriptado de SSH para transferir archivos entre tu computadora y el servidor.

```bash
# Sintaxis: scp [archivo_local] [usuario@ip]:[ruta_destino]
scp smartsolutions.zip deploy@164.92.100.50:~/smartsolutions/

# Copiar un archivo DEL servidor a tu computadora:
scp deploy@164.92.100.50:~/backups/backup.sql ./
```

### Comandos SSH que usarás

| Comando | Qué hace |
|---------|----------|
| `ssh deploy@IP` | Conectarte al servidor |
| `ssh -i ~/.ssh/id_ed25519 deploy@IP` | Conectar con una llave específica |
| `scp archivo deploy@IP:~/ruta/` | Copiar archivo al servidor |
| `exit` | Cerrar la sesión SSH |

---

## 2. Linux / Ubuntu Server

### Qué es

Ubuntu Server es un sistema operativo Linux diseñado para servidores. No tiene interfaz gráfica — todo se maneja por línea de comandos. Es el sistema operativo más popular para servidores web por su estabilidad, seguridad y la enorme comunidad de soporte.

Ubuntu 24.04 LTS significa:
- **24.04**: Lanzado en abril de 2024.
- **LTS** (Long Term Support): Tiene 5 años de actualizaciones de seguridad garantizadas. Esto es fundamental para un servidor de producción.

### Estructura de directorios que necesitas conocer

```
/                       → Raíz del sistema
├── /home/deploy/       → Directorio home de tu usuario "deploy"
│   └── smartsolutions/ → Aquí vivirá tu proyecto
├── /etc/               → Archivos de configuración del sistema
├── /var/log/           → Logs del sistema
└── /usr/local/bin/     → Binarios instalados manualmente
```

### Usuarios y permisos

Linux tiene un sistema de usuarios y permisos muy estricto:

- **root**: El superusuario con acceso total. Nunca debes trabajar como root en producción porque un error puede destruir el sistema completo.
- **deploy** (o el nombre que elijas): Un usuario regular con permisos limitados. Puede ejecutar comandos administrativos temporalmente usando `sudo`.

```bash
# Crear el usuario "deploy"
adduser deploy

# Darle permisos de sudo (administrador temporal)
usermod -aG sudo deploy
```

El flag `-aG sudo` significa: "**a**gregar al **G**rupo sudo". El grupo sudo es un grupo especial cuyos miembros pueden ejecutar cualquier comando anteponiendo `sudo`.

### El comando `sudo`

`sudo` (Super User DO) te permite ejecutar un comando con permisos de root temporalmente. El sistema te pedirá tu contraseña (no la de root) para confirmar.

```bash
# Sin sudo — falla porque un usuario normal no puede instalar paquetes
apt install nginx

# Con sudo — funciona porque eleva tus permisos temporalmente
sudo apt install nginx
```

### El gestor de paquetes `apt`

`apt` (Advanced Package Tool) es el sistema que Ubuntu usa para instalar, actualizar y eliminar software. Funciona descargando paquetes desde repositorios oficiales de Ubuntu.

```bash
# Actualizar la LISTA de paquetes disponibles (no instala nada aún)
sudo apt update

# Actualizar todos los paquetes INSTALADOS a sus versiones más recientes
sudo apt upgrade -y

# El flag -y responde "yes" automáticamente a las confirmaciones

# Instalar un paquete
sudo apt install -y curl wget zip unzip

# Eliminar un paquete
sudo apt remove nombre-paquete
```

Es importante entender la diferencia:
- `apt update` solo actualiza el **índice** (la lista de qué versiones existen).
- `apt upgrade` descarga e instala las **actualizaciones** de los paquetes que ya tienes.

Siempre ejecuta `apt update` antes de `apt upgrade` o `apt install`.

### Comandos de navegación y archivos esenciales

| Comando | Qué hace | Ejemplo |
|---------|----------|---------|
| `cd ruta` | Cambiar de directorio | `cd ~/smartsolutions` |
| `ls` | Listar archivos | `ls -la` (muestra ocultos y permisos) |
| `pwd` | Mostrar directorio actual | `/home/deploy/smartsolutions` |
| `mkdir -p ruta` | Crear directorio (y padres) | `mkdir -p ~/smartsolutions/nginx/conf.d` |
| `nano archivo` | Editar archivo con nano | `nano docker-compose.yml` |
| `cat archivo` | Mostrar contenido de archivo | `cat .env` |
| `cp origen destino` | Copiar archivo | `cp .env .env.backup` |
| `mv origen destino` | Mover/renombrar archivo | `mv app.old app` |
| `rm archivo` | Eliminar archivo | `rm -rf __pycache__/` |
| `chmod +x script.sh` | Hacer un archivo ejecutable | `chmod +x renew-ssl.sh` |
| `unzip archivo.zip -d carpeta/` | Descomprimir ZIP | `unzip smartsolutions.zip -d app/` |

### El editor Nano

Nano es un editor de texto simple que funciona en la terminal. Es el más amigable para principiantes.

Controles esenciales dentro de nano:
- **Ctrl + O** → Guardar (te pide confirmar el nombre, presiona Enter)
- **Ctrl + X** → Salir
- **Ctrl + W** → Buscar texto
- **Ctrl + K** → Cortar línea
- **Ctrl + U** → Pegar línea
- Las flechas del teclado para moverte

---

## 3. UFW (Uncomplicated Firewall)

### Qué es

UFW es una herramienta simplificada para manejar el firewall de Linux (que internamente usa `iptables`, una herramienta mucho más compleja). Un firewall controla qué conexiones de red pueden entrar y salir de tu servidor.

Sin un firewall, todos los puertos de tu servidor estarían expuestos a internet. Esto es peligroso porque cualquier servicio corriendo en cualquier puerto sería accesible públicamente.

### Concepto de puertos

Un puerto es un número (del 1 al 65535) que identifica un servicio específico en un servidor. Piensa en la IP como la dirección de un edificio y el puerto como el número de apartamento.

Puertos estándar que usarás:

| Puerto | Servicio | Por qué lo necesitas |
|--------|----------|---------------------|
| 22 | SSH | Para conectarte al servidor remotamente |
| 80 | HTTP | Para servir tu sitio web (sin encriptación) |
| 443 | HTTPS | Para servir tu sitio web (con encriptación SSL) |
| 5432 | PostgreSQL | Base de datos (NO lo expongas a internet) |
| 8000 | Gunicorn/Django | El servidor de aplicación (solo acceso interno) |

### Cómo funciona UFW

UFW trabaja con reglas simples: cada regla dice "permitir" o "denegar" tráfico en un puerto específico. Por defecto, cuando activas UFW, **bloquea todo el tráfico entrante** excepto lo que explícitamente permitas.

```bash
# Permitir SSH (SIEMPRE hazlo ANTES de activar el firewall,
# o te quedarás fuera del servidor)
sudo ufw allow OpenSSH

# Permitir tráfico web
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Activar el firewall
sudo ufw enable

# Ver qué reglas están activas
sudo ufw status
```

La salida de `ufw status` se ve así:

```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
```

**Advertencia crítica:** Si activas UFW sin permitir SSH primero, perderás acceso al servidor y tendrás que usar la consola de emergencia de DigitalOcean para arreglarlo.

Nota que el puerto 5432 (PostgreSQL) NO se abre en el firewall. Esto es intencional: la base de datos solo necesita ser accesible desde dentro del servidor (los contenedores Docker se comunican entre sí por una red interna). Exponerla a internet sería un riesgo de seguridad grave.

---

## 4. Docker

### Qué es

Docker es una plataforma que permite empaquetar una aplicación junto con todas sus dependencias en un "contenedor". Un contenedor es como una caja aislada que contiene todo lo que la aplicación necesita para funcionar: el sistema operativo base, las librerías, el código y la configuración.

### El problema que resuelve

Sin Docker, tendrías que instalar Python, PostgreSQL, Nginx y todas sus dependencias directamente en el servidor. Esto causa problemas:

- Conflictos de versiones entre proyectos.
- "En mi máquina funciona" — diferencias entre tu computadora y el servidor.
- Instalar y configurar todo manualmente es lento y propenso a errores.
- Actualizar o migrar a otro servidor requiere repetir todo el proceso.

Con Docker, empaquetas cada servicio en su contenedor y sabes que funcionará igual en cualquier servidor.

### Conceptos fundamentales

**Imagen (Image):** Es una plantilla de solo lectura que define qué contiene un contenedor. Piensa en ella como un "molde" o "receta". Por ejemplo, `python:3.11-slim` es una imagen que contiene Python 3.11 sobre un Linux mínimo.

**Contenedor (Container):** Es una instancia en ejecución de una imagen. Si la imagen es el molde, el contenedor es el objeto creado a partir del molde. Puedes tener múltiples contenedores de la misma imagen.

**Dockerfile:** Es un archivo de texto con instrucciones paso a paso para construir una imagen personalizada. Es como una receta de cocina.

**Volumen (Volume):** Es un mecanismo para que los datos persistan más allá del ciclo de vida de un contenedor. Sin volúmenes, cuando destruyes un contenedor, se pierden todos sus datos. Los volúmenes "montan" un directorio del servidor dentro del contenedor.

**Red (Network):** Docker crea redes virtuales para que los contenedores se comuniquen entre sí de forma aislada. Los contenedores en la misma red pueden encontrarse por nombre.

### El Dockerfile explicado línea por línea

```dockerfile
# Imagen base: Python 3.11 sobre Debian "slim" (versión mínima, ~150MB)
FROM python:3.11-slim

# PYTHONUNBUFFERED=1: Los prints de Python aparecen inmediatamente en los logs
# (sin esto, Python almacena la salida en buffer y los logs se retrasan)
ENV PYTHONUNBUFFERED=1

# PYTHONDONTWRITEBYTECODE=1: No crear archivos .pyc
# (son innecesarios en un contenedor y ocupan espacio)
ENV PYTHONDONTWRITEBYTECODE=1

# Establece /app como el directorio de trabajo dentro del contenedor
# Todos los comandos siguientes se ejecutan desde aquí
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar paquetes Python
# gcc: compilador C (algunas librerías Python tienen código C)
# postgresql-client: herramientas para conectar a PostgreSQL
# libpq-dev: librerías de desarrollo de PostgreSQL (necesarias para psycopg2)
# rm -rf /var/lib/apt/lists/*: limpia la caché de apt para reducir tamaño
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia SOLO requirements.txt primero (optimización de caché)
# Docker cachea cada capa. Si el código cambia pero requirements.txt no,
# Docker reutiliza la capa de pip install y ahorra minutos de build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copia todo el código del proyecto
COPY . .

# Crea el directorio donde Django guardará los archivos estáticos compilados
RUN mkdir -p /app/staticfiles

# Ejecuta collectstatic para reunir todos los CSS/JS/imágenes en /app/staticfiles
RUN python manage.py collectstatic --noinput

# Documenta que el contenedor escucha en el puerto 8000
# (es informativo, no abre el puerto realmente)
EXPOSE 8000

# Comando que se ejecuta cuando el contenedor inicia
# Lanza Gunicorn sirviendo la aplicación Django en el puerto 8000 con 3 workers
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

### Comandos Docker esenciales

| Comando | Qué hace |
|---------|----------|
| `docker build -t nombre .` | Construir una imagen desde un Dockerfile |
| `docker run imagen` | Crear y ejecutar un contenedor |
| `docker ps` | Ver contenedores en ejecución |
| `docker ps -a` | Ver todos los contenedores (incluso detenidos) |
| `docker logs contenedor` | Ver logs de un contenedor |
| `docker exec -it contenedor bash` | Abrir una terminal dentro del contenedor |
| `docker stop contenedor` | Detener un contenedor |
| `docker rm contenedor` | Eliminar un contenedor detenido |
| `docker images` | Ver imágenes descargadas |
| `docker system prune -a` | Limpiar todo lo no usado (libera espacio) |

### Cómo Docker aísla los procesos

Cada contenedor tiene su propio filesystem, su propia red interna y sus propios procesos. Un contenedor no puede ver ni afectar a otro contenedor a menos que estén en la misma red Docker y se conecten explícitamente.

En tu caso, tendrás 3 contenedores:

```
┌─────────────────────────────────────────────┐
│               Servidor (Droplet)             │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  Nginx   │  │  Django   │  │ PostgreSQL│  │
│  │  :80/443 │→ │  :8000   │→ │  :5432    │  │
│  └──────────┘  └──────────┘  └───────────┘  │
│       ↑                                      │
│    Internet         Red interna Docker       │
└─────────────────────────────────────────────┘
```

---

## 5. Docker Compose

### Qué es

Docker Compose es una herramienta que permite definir y manejar múltiples contenedores Docker como un solo servicio. En lugar de ejecutar varios comandos `docker run` con flags complicados, defines todo en un archivo YAML y lo levantas con un solo comando.

### El archivo docker-compose.yml explicado

```yaml
# Versión del formato de Docker Compose
version: '3.8'

services:
  # ═══════════════════════════════════════════
  # SERVICIO: Base de datos PostgreSQL
  # ═══════════════════════════════════════════
  db:
    # Imagen oficial de PostgreSQL versión 16, variante Alpine (ligera, ~80MB)
    image: postgres:16-alpine

    # Nombre fijo del contenedor (sino Docker genera uno aleatorio)
    container_name: smartsolutions_db

    # Política de reinicio: si el contenedor se cae, Docker lo reinicia
    # "always" significa que se reinicia incluso si el servidor se reinicia
    restart: always

    # Variables de entorno que PostgreSQL lee al iniciar
    environment:
      POSTGRES_DB: ${DB_NAME}         # Nombre de la BD (viene del .env)
      POSTGRES_USER: ${DB_USER}       # Usuario de la BD (viene del .env)
      POSTGRES_PASSWORD: ${DB_PASSWORD} # Contraseña (viene del .env)

    # Volumen: mapea una carpeta del servidor al contenedor
    # Los datos de PostgreSQL se guardan en ./postgres-data del servidor
    # Así si destruyes el contenedor, los datos sobreviven
    volumes:
      - ./postgres-data:/var/lib/postgresql/data

    # Conecta este contenedor a la red interna
    networks:
      - smartsolutions_network

  # ═══════════════════════════════════════════
  # SERVICIO: Aplicación Django
  # ═══════════════════════════════════════════
  web:
    # En vez de usar una imagen existente, construye una desde el Dockerfile
    build: ./app

    container_name: smartsolutions_web
    restart: always

    # Carga todas las variables del archivo .env en el contenedor
    env_file:
      - .env

    volumes:
      # Monta el código fuente (permite ver cambios sin reconstruir)
      - ./app:/app
      # Volúmenes nombrados para static y media (compartidos con Nginx)
      - static_volume:/app/staticfiles
      - media_volume:/app/media

    # Este servicio depende de "db" — Docker levanta db primero
    # NOTA: depends_on solo espera a que el contenedor INICIE,
    # no a que PostgreSQL esté listo para recibir conexiones
    depends_on:
      - db

    networks:
      - smartsolutions_network

    # Comando que ejecuta al iniciar: migra la BD, recopila estáticos
    # y luego lanza Gunicorn
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3"

  # ═══════════════════════════════════════════
  # SERVICIO: Nginx (reverse proxy)
  # ═══════════════════════════════════════════
  nginx:
    image: nginx:alpine
    container_name: smartsolutions_nginx
    restart: always

    # Puertos: mapea puertos del SERVIDOR a puertos del CONTENEDOR
    # "80:80" significa: puerto 80 del servidor → puerto 80 de Nginx
    ports:
      - "80:80"
      - "443:443"

    volumes:
      # Configuración de Nginx (solo lectura con :ro)
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      # Archivos estáticos de Django (solo lectura)
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
      # Certificados SSL
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro

    depends_on:
      - web

    networks:
      - smartsolutions_network

# Volúmenes nombrados: Docker los gestiona y persisten entre reinicios
volumes:
  static_volume:
  media_volume:

# Red personalizada: todos los servicios pueden comunicarse por nombre
# Ejemplo: Django conecta a PostgreSQL usando "db" como hostname
networks:
  smartsolutions_network:
    driver: bridge
```

### Sintaxis YAML básica

YAML es el formato del archivo docker-compose.yml. Las reglas son:

- La indentación se hace con **espacios** (nunca tabulaciones). Usa 2 espacios por nivel.
- Los pares clave-valor se escriben como `clave: valor`.
- Las listas se escriben con guiones (`-`).
- Los comentarios empiezan con `#`.
- `${VARIABLE}` se reemplaza con el valor de la variable de entorno.

```yaml
# Ejemplo de YAML
nombre: "SmartSolutions"    # String
puerto: 8000                # Número
activo: true                # Booleano

# Lista
servicios:
  - nginx
  - django
  - postgres

# Objeto anidado
base_datos:
  host: db
  puerto: 5432
```

Un error de indentación rompe todo el archivo. Si algo no funciona, verifica que la indentación sea consistente.

### Comandos Docker Compose esenciales

| Comando | Qué hace |
|---------|----------|
| `docker-compose up -d` | Levantar todos los servicios en segundo plano |
| `docker-compose down` | Detener y eliminar todos los contenedores |
| `docker-compose ps` | Ver estado de los servicios |
| `docker-compose logs -f web` | Ver logs en tiempo real de un servicio |
| `docker-compose build web` | Reconstruir la imagen de un servicio |
| `docker-compose restart web` | Reiniciar un servicio |
| `docker-compose exec web bash` | Abrir terminal dentro de un contenedor |
| `docker-compose exec web python manage.py migrate` | Ejecutar comando Django |
| `docker-compose up -d --force-recreate web` | Recrear un servicio con cambios |

El flag `-d` (detached) es importante: hace que los contenedores se ejecuten en segundo plano. Sin `-d`, la terminal queda bloqueada mostrando logs y si la cierras, los contenedores se detienen.

---

## 6. PostgreSQL

### Qué es

PostgreSQL (a menudo abreviado como "Postgres") es un sistema de gestión de bases de datos relacional. Es donde tu aplicación Django almacena todos sus datos: usuarios, servicios, testimonios, mensajes de contacto, etc.

Django puede funcionar con SQLite (un archivo local), pero en producción se usa PostgreSQL porque es más robusto, soporta acceso concurrente (múltiples usuarios al mismo tiempo), tiene mejor rendimiento con grandes volúmenes de datos y ofrece herramientas avanzadas de backup y recuperación.

### Por qué se ejecuta en Docker

En vez de instalar PostgreSQL directamente en el servidor (lo que requiere configurar usuarios del sistema, rutas de datos, permisos, etc.), lo ejecutamos dentro de un contenedor Docker. Las ventajas son:

- Instalación instantánea: `docker-compose up -d db` y listo.
- Aislamiento: PostgreSQL corre en su propio entorno sin afectar el servidor.
- Portabilidad: la misma configuración funciona en cualquier servidor.
- Versión fija: siempre usas PostgreSQL 16, sin importar qué versión ofrezca Ubuntu.

### Cómo Django se conecta a PostgreSQL

Django usa las variables de entorno del archivo `.env` para conectarse:

```python
# En settings.py de Django (ya configurado en tu proyecto)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),      # smartsolutions
        'USER': os.environ.get('DB_USER'),       # smartsolutions
        'PASSWORD': os.environ.get('DB_PASSWORD'), # tu-contraseña
        'HOST': os.environ.get('DB_HOST'),       # "db" (nombre del servicio Docker)
        'PORT': os.environ.get('DB_PORT'),       # 5432
    }
}
```

El `HOST` es `db` (no `localhost`) porque Docker Compose crea una red interna donde cada servicio es accesible por su nombre. El contenedor Django se conecta al contenedor PostgreSQL usando `db:5432`.

### Volumen de datos

```yaml
volumes:
  - ./postgres-data:/var/lib/postgresql/data
```

Esta línea es crucial. Mapea el directorio `postgres-data` de tu servidor al directorio donde PostgreSQL almacena sus datos dentro del contenedor. Esto significa que si el contenedor se destruye, los datos permanecen en el servidor. Sin este volumen, al eliminar el contenedor perderías toda la base de datos.

### Backup y restauración

```bash
# Crear un backup (volcado SQL completo)
docker-compose exec -T db pg_dump -U smartsolutions smartsolutions > backup.sql

# El flag -T desactiva la terminal interactiva (necesario para redireccionar la salida)

# Restaurar un backup
docker-compose exec -T db psql -U smartsolutions smartsolutions < backup.sql

# Conectarte a la consola interactiva de PostgreSQL
docker-compose exec db psql -U smartsolutions -d smartsolutions
```

Dentro de la consola `psql` puedes ejecutar SQL directamente:

```sql
-- Ver todas las tablas
\dt

-- Ver datos de una tabla
SELECT * FROM contact_messages LIMIT 10;

-- Salir
\q
```

---

## 7. Django en Producción

### Diferencias entre desarrollo y producción

En desarrollo (`python manage.py runserver`), Django usa un servidor web simple diseñado para desarrollo. En producción, hay cambios fundamentales:

| Aspecto | Desarrollo | Producción |
|---------|-----------|------------|
| Servidor web | `runserver` (integrado) | Gunicorn (profesional) |
| DEBUG | `True` (muestra errores detallados) | `False` (oculta errores) |
| Archivos estáticos | Django los sirve | Nginx los sirve |
| Base de datos | SQLite (archivo) | PostgreSQL (servidor) |
| HTTPS | No | Sí (Let's Encrypt) |
| SECRET_KEY | Puede estar en el código | DEBE estar en variable de entorno |

### DEBUG = False

Cuando `DEBUG=True`, Django muestra páginas de error detalladas con el stack trace, las variables de entorno y hasta fragmentos de código. Esto es extremadamente peligroso en producción porque un atacante podría obtener información sensible.

Con `DEBUG=False`:
- Los errores muestran una página genérica "500 Server Error".
- Los archivos estáticos NO se sirven por Django (necesitas Nginx).
- `ALLOWED_HOSTS` debe estar configurado correctamente.

### ALLOWED_HOSTS

Es una lista de dominios/IPs desde los que Django acepta peticiones. Es una protección contra ataques de tipo "Host Header Injection".

```python
# En .env
ALLOWED_HOSTS=smartsolutions.com.ve,www.smartsolutions.com.ve,164.92.100.50
```

Si alguien intenta acceder a tu servidor usando un dominio diferente, Django rechaza la petición con un error 400.

### SECRET_KEY

Es una cadena aleatoria que Django usa para firmar cookies, tokens CSRF, sesiones y otros datos criptográficos. Si alguien la descubre, podría falsificar sesiones de usuario y obtener acceso de administrador.

Reglas:
- Nunca la pongas en el código fuente ni en Git.
- Debe ser larga y aleatoria (mínimo 50 caracteres).
- Guárdala en el archivo `.env`.

```bash
# Generar una SECRET_KEY segura
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### collectstatic

En producción, Django no sirve archivos estáticos (CSS, JavaScript, imágenes). El comando `collectstatic` recopila todos los archivos estáticos de cada app de Django y los copia a un directorio central (`/app/staticfiles/`). Luego, Nginx sirve esos archivos directamente, lo cual es mucho más eficiente.

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Migraciones

Las migraciones son la forma en que Django sincroniza los modelos de Python con las tablas de la base de datos.

```bash
# Crear archivos de migración (detecta cambios en models.py)
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones (ejecuta los cambios en la base de datos)
docker-compose exec web python manage.py migrate
```

El comando `migrate` en el `docker-compose.yml` se ejecuta automáticamente cada vez que el contenedor inicia, asegurando que la BD siempre esté al día.

---

## 8. Gunicorn

### Qué es

Gunicorn (Green Unicorn) es un servidor WSGI para Python. WSGI (Web Server Gateway Interface) es el estándar que define cómo un servidor web se comunica con una aplicación Python.

El servidor de desarrollo de Django (`runserver`) solo puede manejar una petición a la vez y no está diseñado para producción. Gunicorn puede manejar múltiples peticiones simultáneamente usando "workers".

### Cómo funciona

```
Internet → Nginx → Gunicorn → Django → Respuesta
                    ↓
            Worker 1 (proceso Python)
            Worker 2 (proceso Python)
            Worker 3 (proceso Python)
```

Cada worker es un proceso independiente de Python que puede manejar una petición. Si tienes 3 workers, puedes manejar 3 peticiones simultáneamente. Los workers son gestionados por un proceso master que distribuye las peticiones.

### El comando de inicio

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Desglose:
- `config.wsgi:application` → Apunta al archivo `config/wsgi.py` de tu proyecto Django, que contiene el objeto `application` que WSGI necesita.
- `--bind 0.0.0.0:8000` → Escucha en todas las interfaces de red del contenedor, en el puerto 8000.
- `--workers 3` → Lanza 3 procesos worker.

La fórmula recomendada para calcular workers es `(2 × CPUs) + 1`. Con 1 CPU en el droplet de $6, serían 3 workers.

### Por qué Gunicorn no sirve el sitio directamente

Gunicorn es excelente procesando código Python, pero no es eficiente sirviendo archivos estáticos, manejando conexiones lentas, o terminando SSL. Para eso está Nginx al frente.

---

## 9. Nginx

### Qué es

Nginx (pronunciado "engine-x") es un servidor web y reverse proxy de alto rendimiento. En tu stack, Nginx tiene tres funciones principales:

1. **Reverse proxy:** Recibe las peticiones de internet y las reenvía a Gunicorn.
2. **Servidor de archivos estáticos:** Sirve CSS, JavaScript e imágenes directamente, sin pasar por Django.
3. **Terminación SSL:** Maneja la encriptación HTTPS, liberando a Gunicorn de esa carga.

### Qué es un reverse proxy

Un reverse proxy es un servidor que se coloca frente a tu aplicación y actúa como intermediario. El usuario nunca habla directamente con Django — siempre habla con Nginx, que reenvía la petición internamente.

```
Usuario → Internet → Nginx (puerto 80/443) → Gunicorn (puerto 8000) → Django
                       ↓
                  Archivos estáticos
                  (CSS, JS, imágenes)
                  servidos directamente
```

Ventajas:
- **Rendimiento:** Nginx sirve archivos estáticos 10-100x más rápido que Django.
- **Seguridad:** Oculta la estructura interna de tu aplicación.
- **Buffer:** Nginx absorbe conexiones lentas y las envía a Gunicorn solo cuando están listas.
- **Compresión:** Comprime respuestas con gzip antes de enviarlas al usuario.
- **Caché:** Los archivos estáticos se cachean en el navegador por 30 días.

### La configuración de Nginx explicada

#### Archivo principal: nginx.conf

```nginx
# El usuario bajo el que corre Nginx dentro del contenedor
user nginx;

# auto = un worker por CPU (en tu caso, 1)
worker_processes auto;

# Dónde se guardan los logs de errores
error_log /var/log/nginx/error.log warn;

events {
    # Máximo de conexiones simultáneas por worker
    worker_connections 1024;
}

http {
    # Carga los tipos MIME (para que Nginx sepa que .css es text/css, etc.)
    include /etc/nginx/mime.types;

    # Activar compresión gzip (reduce el tamaño de las respuestas ~70%)
    gzip on;
    gzip_vary on;
    gzip_comp_level 6;  # Nivel de compresión (1=rápido, 9=máxima compresión)
    gzip_types text/plain text/css application/json application/javascript;

    # Tamaño máximo de archivos que se pueden subir (20 megabytes)
    client_max_body_size 20M;

    # Cargar configuraciones de sitios individuales
    include /etc/nginx/conf.d/*.conf;
}
```

#### Archivo del sitio: conf.d/smartsolutions.conf

```nginx
# Bloque HTTP: redirige todo a HTTPS
server {
    listen 80;  # Escucha en puerto 80 (HTTP)
    server_name tu-dominio.com www.tu-dominio.com;

    # Excepción para Let's Encrypt (necesita HTTP para verificar el dominio)
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirige todo lo demás a HTTPS con código 301 (redirección permanente)
    location / {
        return 301 https://$host$request_uri;
    }
}

# Bloque HTTPS: el servidor principal
server {
    listen 443 ssl http2;  # Escucha en 443 con SSL y HTTP/2
    server_name tu-dominio.com www.tu-dominio.com;

    # Certificados SSL (generados por Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    # Headers de seguridad que protegen contra ataques comunes
    # HSTS: fuerza al navegador a usar HTTPS siempre
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    # Previene que el sitio se cargue dentro de un iframe (anti-clickjacking)
    add_header X-Frame-Options "SAMEORIGIN" always;
    # Previene que el navegador "adivine" el tipo de contenido
    add_header X-Content-Type-Options "nosniff" always;

    # PETICIONES DINÁMICAS: se reenvían a Django/Gunicorn
    location / {
        proxy_pass http://web:8000;  # "web" es el nombre del servicio Docker
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # ARCHIVOS ESTÁTICOS: Nginx los sirve directamente (no pasan por Django)
    location /static/ {
        alias /app/staticfiles/;   # Ruta dentro del contenedor Nginx
        expires 30d;               # El navegador los cachea por 30 días
        add_header Cache-Control "public, immutable";
        access_log off;            # No registrar peticiones de estáticos en logs
    }

    # ARCHIVOS MEDIA: uploads de usuarios (imágenes, documentos)
    location /media/ {
        alias /app/media/;
        expires 7d;
    }
}
```

### Cómo Nginx se comunica con Django

La directiva `proxy_pass http://web:8000` es la pieza clave. `web` es el nombre del servicio Django en docker-compose.yml. Docker Compose crea una red interna donde cada servicio es resoluble por su nombre, así que Nginx puede encontrar a Django usando el hostname `web`.

Los `proxy_set_header` son importantes porque cuando Nginx reenvía una petición, Django necesita saber la información original del cliente:

- `X-Real-IP`: La IP real del usuario (sin esto, Django solo vería la IP del contenedor Nginx).
- `X-Forwarded-Proto`: Si el usuario conectó por HTTP o HTTPS (Django necesita esto para generar URLs correctas).

---

## 10. SSL/TLS y Let's Encrypt

### Qué es SSL/TLS

SSL (Secure Sockets Layer) y su sucesor TLS (Transport Layer Security) son protocolos de encriptación que protegen la comunicación entre el navegador del usuario y tu servidor. Cuando ves el candado verde y `https://` en la barra del navegador, la conexión usa TLS.

Sin SSL, todo el tráfico viaja en texto plano. Esto significa que cualquier persona en la misma red (WiFi pública, proveedor de internet) podría ver contraseñas, formularios y datos personales.

### Cómo funciona (simplificado)

1. El navegador se conecta a `https://tu-dominio.com`.
2. Tu servidor envía su **certificado SSL** (que incluye la llave pública).
3. El navegador verifica que el certificado sea válido y emitido por una autoridad confiable.
4. Se establece un canal encriptado usando criptografía asimétrica.
5. Toda la comunicación posterior viaja encriptada.

### Qué es un certificado SSL

Un certificado SSL es un archivo digital que demuestra que tu servidor es realmente quien dice ser. Contiene tu dominio, la autoridad que lo emitió (CA - Certificate Authority) y una llave criptográfica.

Los certificados tienen dos archivos importantes:
- `fullchain.pem` → El certificado público (se comparte con todos los navegadores).
- `privkey.pem` → La llave privada (NUNCA se comparte, solo la usa tu servidor).

### Let's Encrypt y Certbot

Let's Encrypt es una autoridad de certificación que emite certificados SSL **gratuitos**. Antes de Let's Encrypt, los certificados costaban entre $50-$300 al año.

Certbot es la herramienta que automatiza el proceso de obtener y renovar certificados de Let's Encrypt.

### El proceso de verificación (challenge)

Cuando solicitas un certificado, Let's Encrypt necesita verificar que realmente controlas el dominio. El método más común es el **HTTP challenge**:

1. Certbot coloca un archivo temporal en `/.well-known/acme-challenge/` de tu servidor.
2. Let's Encrypt intenta acceder a `http://tu-dominio.com/.well-known/acme-challenge/archivo`.
3. Si puede leerlo, prueba que controlas el dominio.
4. Let's Encrypt emite el certificado.

Por eso la configuración de Nginx tiene este bloque:

```nginx
location /.well-known/acme-challenge/ {
    root /var/www/certbot;
}
```

### Renovación automática

Los certificados de Let's Encrypt duran 90 días. El script `renew-ssl.sh` configurado en cron ejecuta `certbot renew`, que verifica si el certificado está próximo a vencer y lo renueva automáticamente.

```bash
# El cron ejecuta esto cada día a las 3am
0 3 * * * /home/deploy/smartsolutions/renew-ssl.sh
```

Certbot solo renueva si faltan menos de 30 días para el vencimiento, así que ejecutarlo diariamente es seguro y no genera peticiones innecesarias.

---

## 11. DNS (Sistema de Nombres de Dominio)

### Qué es

DNS es el sistema que traduce nombres de dominio legibles por humanos (como `smartsolutions.com.ve`) a direcciones IP (como `164.92.100.50`). Sin DNS, tendrías que recordar la dirección IP de cada sitio web.

### Cómo funciona una consulta DNS

Cuando un usuario escribe `smartsolutions.com.ve` en su navegador:

1. El navegador pregunta al servidor DNS del proveedor de internet.
2. Si no tiene la respuesta, pregunta a los servidores raíz de internet.
3. Los servidores raíz dirigen a los servidores de `.com.ve`.
4. Los servidores de `.com.ve` dirigen al DNS de tu proveedor de dominio.
5. Tu proveedor de dominio responde con la IP `164.92.100.50`.
6. El navegador se conecta a esa IP.

Todo esto sucede en milisegundos.

### Registros DNS que necesitas configurar

**Registro A (Address):** Asocia un dominio con una dirección IP IPv4.

```
Tipo: A
Nombre: @              → significa "el dominio raíz" (smartsolutions.com.ve)
Valor: 164.92.100.50   → la IP de tu droplet
TTL: 3600              → tiempo en segundos que se cachea (1 hora)

Tipo: A
Nombre: www            → el subdominio www (www.smartsolutions.com.ve)
Valor: 164.92.100.50   → la misma IP
TTL: 3600
```

**¿Qué es TTL?** TTL (Time To Live) indica cuánto tiempo los servidores DNS intermedios guardan en caché tu registro. Un TTL de 3600 (1 hora) significa que si cambias la IP, tomará hasta 1 hora para que el cambio se propague globalmente. Un TTL bajo (300 = 5 minutos) propaga cambios más rápido pero genera más consultas DNS.

### Propagación DNS

Cuando creas o cambias registros DNS, el cambio no es instantáneo. Cada servidor DNS del mundo necesita actualizar su caché. Esto puede tomar desde 5 minutos hasta 48 horas, aunque típicamente es menos de 1 hora.

Para verificar la propagación:

```bash
# Verificar que el dominio apunta a tu IP
nslookup smartsolutions.com.ve

# También puedes usar dig (más detallado)
dig smartsolutions.com.ve

# Online: https://www.whatsmydns.net/
```

### Orden correcto: DNS antes de SSL

Debes configurar los registros DNS y esperar a que propaguen **antes** de solicitar el certificado SSL. Let's Encrypt necesita poder acceder a tu servidor a través del dominio para verificar que lo controlas.

---

## 12. DigitalOcean (Infraestructura Cloud)

### Qué es

DigitalOcean es un proveedor de infraestructura en la nube que te alquila servidores virtuales. En vez de comprar un servidor físico (que cuesta miles de dólares y necesita mantenimiento), alquilas una máquina virtual por $6/mes.

### Qué es un Droplet

Un "Droplet" es el nombre que DigitalOcean le da a sus máquinas virtuales. Cuando creas un Droplet, DigitalOcean asigna recursos de un servidor físico grande y te da una porción dedicada.

El Droplet de $6/mes incluye:
- **1 GB RAM:** Suficiente para Django + PostgreSQL + Nginx en Docker. Django típicamente usa 50-200MB por worker de Gunicorn.
- **1 vCPU:** Un núcleo de procesador virtual. Suficiente para un sitio con tráfico bajo-medio.
- **25 GB SSD:** Almacenamiento en disco de estado sólido. Suficiente para el código, la base de datos y archivos media.
- **1 TB de transferencia:** El total de datos que puede enviar tu servidor al mes. Para un sitio web típico, esto es más que suficiente.

### Elegir la región

La región determina la ubicación física del servidor. La latencia (el tiempo que tarda una petición en llegar) depende de la distancia física.

Para usuarios en Venezuela:
- **New York (NYC):** ~30-50ms de latencia. La mejor opción.
- **San Francisco:** ~80-100ms. Funcional pero más lento.
- **Ámsterdam/Frankfurt:** ~150-200ms. Demasiado lejos.

### Escalamiento futuro

Si tu sitio crece y necesita más recursos, puedes "redimensionar" el Droplet desde el panel de DigitalOcean. Esto cambia el plan a uno más potente (más RAM, más CPU) con un clic y un reinicio breve. Los datos se conservan.

---

## 13. Cron (Tareas Programadas)

### Qué es

Cron es el servicio de Linux que ejecuta tareas automáticamente según un horario definido. Lo usarás para dos cosas: hacer backups diarios de la base de datos y renovar el certificado SSL.

### Sintaxis de crontab

El formato de una entrada en crontab es:

```
┌───────────── minuto (0-59)
│ ┌───────────── hora (0-23)
│ │ ┌───────────── día del mes (1-31)
│ │ │ ┌───────────── mes (1-12)
│ │ │ │ ┌───────────── día de la semana (0-7, donde 0 y 7 = domingo)
│ │ │ │ │
* * * * * comando-a-ejecutar
```

Ejemplos:

| Expresión | Significado |
|-----------|-------------|
| `0 2 * * *` | Todos los días a las 2:00 AM |
| `0 3 * * *` | Todos los días a las 3:00 AM |
| `*/15 * * * *` | Cada 15 minutos |
| `0 0 * * 0` | Todos los domingos a medianoche |
| `0 2 1 * *` | El día 1 de cada mes a las 2:00 AM |

### Cómo editar crontab

```bash
# Abrir el editor de crontab (la primera vez te pedirá elegir editor, elige nano)
crontab -e

# Ver tareas programadas actuales
crontab -l
```

### Las tareas que configurarás

```bash
# Backup de base de datos: cada día a las 2:00 AM
0 2 * * * /home/deploy/backup-db.sh >> /home/deploy/backup.log 2>&1

# Renovación SSL: cada día a las 3:00 AM
0 3 * * * /home/deploy/smartsolutions/renew-ssl.sh >> /home/deploy/smartsolutions/ssl-renew.log 2>&1
```

La parte `>> archivo.log 2>&1` redirige tanto la salida normal (`stdout`) como los errores (`stderr`) a un archivo de log. Esto es útil para diagnosticar problemas si algo falla silenciosamente.

---

## 14. Variables de Entorno y Archivos .env

### Qué son las variables de entorno

Las variables de entorno son pares clave-valor que configuran el comportamiento de un programa. En vez de poner valores sensibles (contraseñas, API keys) directamente en el código, los pones en variables de entorno que el código lee en tiempo de ejecución.

### Por qué se usan

1. **Seguridad:** Las contraseñas y llaves secretas nunca se incluyen en el código fuente ni en el repositorio Git.
2. **Flexibilidad:** Puedes tener diferentes configuraciones para desarrollo, staging y producción sin cambiar código.
3. **Estándar de la industria:** Los 12-Factor App (una metodología de referencia para aplicaciones modernas) establecen que la configuración debe estar en variables de entorno.

### El archivo .env

El archivo `.env` es donde defines las variables de entorno. Docker Compose lo lee automáticamente gracias a `env_file: - .env`.

```bash
# Django
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
DEBUG=False
ALLOWED_HOSTS=smartsolutions.com.ve,www.smartsolutions.com.ve,164.92.100.50

# Base de datos
DB_NAME=smartsolutions
DB_USER=smartsolutions
DB_PASSWORD=contraseña-segura-de-la-base-de-datos
DB_HOST=db
DB_PORT=5432

# Email (Resend)
RESEND_API_KEY=re_xxxxxxxxxxxxx
DEFAULT_FROM_EMAIL=noreply@smartsolutions.com.ve
CONTACT_EMAIL=simon@smartsolutions.com.ve

# Sitio
SITE_URL=https://smartsolutions.com.ve
```

### Seguridad del archivo .env

El archivo `.env` contiene las credenciales más sensibles de tu aplicación. Reglas estrictas:

- **Nunca lo subas a Git.** Agrega `.env` a `.gitignore`.
- **Nunca lo compartas por canales inseguros** (email, WhatsApp, etc.).
- **Haz una copia de seguridad** en un lugar seguro fuera del servidor.
- **Permisos restrictivos:** solo tu usuario debe poder leerlo.

```bash
# Restringir permisos: solo el dueño puede leer/escribir
chmod 600 .env
```

---

## 15. Cómo Encajan Todas las Piezas

### Arquitectura completa del deploy

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET                                  │
│                                                                  │
│  Usuario escribe: https://smartsolutions.com.ve                  │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────┐                                                 │
│  │     DNS     │  Traduce "smartsolutions.com.ve" → 164.92.X.X  │
│  └──────┬──────┘                                                 │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────┐                                                 │
│  │   Firewall  │  UFW: solo permite puertos 22, 80 y 443        │
│  │    (UFW)    │                                                 │
│  └──────┬──────┘                                                 │
│         │                                                        │
└─────────┼────────────────────────────────────────────────────────┘
          │
┌─────────┼────────────────────────────────────────────────────────┐
│         │          DROPLET (Servidor DigitalOcean)                │
│         │          Ubuntu 24.04 LTS                              │
│         │                                                        │
│  ┌──────┼─────────────────── Docker Network ──────────────────┐  │
│  │      ▼                                                     │  │
│  │  ┌──────────────────┐                                      │  │
│  │  │      NGINX       │  Puerto 80 → redirige a 443         │  │
│  │  │  (Puerto 80/443) │  Puerto 443 → SSL + reverse proxy   │  │
│  │  └────────┬─────────┘                                      │  │
│  │           │                                                │  │
│  │     ┌─────┴──────┐                                         │  │
│  │     │            │                                         │  │
│  │     ▼            ▼                                         │  │
│  │  /static/     Todo lo                                      │  │
│  │  /media/      demás                                        │  │
│  │  (archivos)      │                                         │  │
│  │  ← Nginx los     │                                         │  │
│  │  sirve directo    ▼                                        │  │
│  │              ┌──────────────────┐                           │  │
│  │              │    GUNICORN      │                           │  │
│  │              │   (Puerto 8000)  │                           │  │
│  │              │   3 workers      │                           │  │
│  │              │                  │                           │  │
│  │              │  ┌────────────┐  │                           │  │
│  │              │  │   DJANGO   │  │                           │  │
│  │              │  │  (tu app)  │  │                           │  │
│  │              │  └─────┬──────┘  │                           │  │
│  │              └────────┼─────────┘                           │  │
│  │                       │                                    │  │
│  │                       ▼                                    │  │
│  │              ┌──────────────────┐                           │  │
│  │              │   POSTGRESQL     │                           │  │
│  │              │  (Puerto 5432)   │                           │  │
│  │              │  Base de datos   │                           │  │
│  │              └──────────────────┘                           │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                      │
│  │    CRON JOBS     │  │   CERTBOT        │                      │
│  │ • Backup BD 2am  │  │ • Renueva SSL    │                      │
│  │ • Renew SSL 3am  │  │   cada 90 días   │                      │
│  └──────────────────┘  └──────────────────┘                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Flujo de una petición paso a paso

Imaginemos que un usuario visita `https://smartsolutions.com.ve/servicios/`:

1. **DNS:** El navegador traduce `smartsolutions.com.ve` a `164.92.100.50`.
2. **Firewall:** UFW permite la conexión porque es al puerto 443 (HTTPS).
3. **Nginx (SSL):** Recibe la petición encriptada, la desencripta usando el certificado SSL.
4. **Nginx (routing):** Ve que la URL es `/servicios/` (no `/static/` ni `/media/`), así que la reenvía a Gunicorn.
5. **Gunicorn:** Recibe la petición HTTP y la asigna a un worker disponible.
6. **Django:** Procesa la URL, ejecuta la vista correspondiente, consulta PostgreSQL para obtener la lista de servicios, y renderiza la plantilla HTML.
7. **Respuesta:** Django devuelve el HTML a Gunicorn → Gunicorn lo devuelve a Nginx → Nginx lo encripta con SSL → el navegador lo recibe y lo muestra.
8. **Estáticos:** El HTML referencia archivos CSS/JS. El navegador hace peticiones separadas para `/static/css/style.css`, etc. Nginx las sirve directamente sin involucrar a Django.

### Flujo de un deploy de cambios

Cuando hagas cambios en el código:

1. Haces los cambios en tu computadora local.
2. Comprimes el proyecto y lo subes al servidor con SCP.
3. Reconstruyes la imagen Docker: `docker-compose build web`.
4. Recreás el contenedor: `docker-compose up -d --force-recreate web`.
5. El nuevo contenedor ejecuta migraciones y recopila estáticos automáticamente.
6. Nginx detecta al nuevo contenedor y comienza a enviarle peticiones.

### Estructura final de archivos en el servidor

```
/home/deploy/smartsolutions/
├── docker-compose.yml          ← Orquesta todos los servicios
├── .env                        ← Variables de entorno (secretas)
├── app/                        ← Tu proyecto Django
│   ├── Dockerfile              ← Instrucciones para construir la imagen
│   ├── manage.py
│   ├── config/                 ← Configuración Django (settings, urls, wsgi)
│   ├── apps/                   ← Tus aplicaciones Django
│   ├── templates/              ← Plantillas HTML
│   ├── static/                 ← Archivos estáticos fuente
│   ├── requirements.txt        ← Dependencias Python
│   └── staticfiles/            ← Archivos estáticos compilados (generado)
├── nginx/
│   ├── nginx.conf              ← Configuración general de Nginx
│   └── conf.d/
│       └── smartsolutions.conf ← Configuración del sitio
├── certbot/
│   ├── conf/                   ← Certificados SSL (generado por Certbot)
│   └── www/                    ← Archivos de verificación Let's Encrypt
├── postgres-data/              ← Datos de PostgreSQL (generado)
├── renew-ssl.sh                ← Script de renovación SSL
└── backup-db.sh                ← Script de backup (en ~/backup-db.sh)
```

---

## Resumen de Tecnologías

| Tecnología | Rol en el deploy | Sin ella... |
|------------|-----------------|-------------|
| **SSH** | Acceso remoto al servidor | No podrías controlar el servidor |
| **Ubuntu** | Sistema operativo del servidor | No habría servidor |
| **UFW** | Firewall (seguridad de red) | Todos los puertos estarían expuestos |
| **Docker** | Empaquetar cada servicio aislado | Instalarías todo manualmente con conflictos |
| **Docker Compose** | Orquestar múltiples contenedores | Ejecutarías comandos docker largos |
| **PostgreSQL** | Base de datos relacional | No se almacenaría nada |
| **Django** | Tu aplicación web (lógica de negocio) | No habría sitio web |
| **Gunicorn** | Servidor de aplicación Python | Django no podría servir peticiones en producción |
| **Nginx** | Reverse proxy, estáticos, SSL | Sin estáticos rápidos, sin HTTPS, sin compresión |
| **Let's Encrypt** | Certificados SSL gratuitos | El sitio no tendría HTTPS (inseguro) |
| **DNS** | Traducción dominio → IP | Los usuarios tendrían que memorizar la IP |
| **DigitalOcean** | Infraestructura (servidor físico) | Necesitarías tu propio servidor |
| **Cron** | Tareas automáticas | Backups y renovación SSL manuales |
| **Variables .env** | Configuración segura | Contraseñas en el código fuente |
