# 🚀 Guía de Instalación - SmartSolutions VE

## Estado Actual del Proyecto
- ✅ Backend Django completo y funcional
- ❌ Frontend HTML sin integrar a Django templates
- ❌ Base de datos sin configurar

---

## OPCIÓN 1: Arranque Rápido (Backend + Admin) - SQLite

Esta opción te permite ver el admin panel funcionando en 5 minutos usando SQLite.

### Paso 1: Crear entorno virtual
```bash
cd "smartsolutions/"

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

### Paso 2: Instalar dependencias
```bash
# Modificar requirements.txt temporalmente (comentar PostgreSQL)
# Cambiar: psycopg2-binary==2.9.9
# Por: # psycopg2-binary==2.9.9

pip install Django==5.0.4 gunicorn==22.0.0 python-decouple==3.8 resend==2.3.0 django-unfold==0.36.0 Pillow==10.3.0 django-cors-headers==4.3.1 whitenoise==6.6.0 django-extensions==3.2.3
```

### Paso 3: Crear archivo .env
```bash
cat > .env << 'EOF'
# Django
SECRET_KEY=django-insecure-desarrollo-local-no-usar-en-produccion-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos SQLite (por defecto Django usa SQLite si no configuramos PostgreSQL)
# Comentar las siguientes líneas para usar SQLite:
# DB_NAME=smartsolutions
# DB_USER=smartsolutions
# DB_PASSWORD=smartsolutions
# DB_HOST=localhost
# DB_PORT=5432

# Email (Resend - dejar vacío para desarrollo)
RESEND_API_KEY=
DEFAULT_FROM_EMAIL=noreply@smartsolutions.com.ve
CONTACT_EMAIL=tu@email.com

# URL del sitio
SITE_URL=http://localhost:8000
EOF
```

### Paso 4: Modificar settings.py temporalmente para SQLite
```bash
# Editar config/settings.py y reemplazar la sección DATABASES por:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Paso 5: Crear migraciones y base de datos
```bash
# Crear migraciones
python manage.py makemigrations core
python manage.py makemigrations landing

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
# Usuario: admin
# Email: admin@smartsolutions.com.ve
# Password: (elige una contraseña)
```

### Paso 6: Crear template temporal para la landing
```bash
# Corregir estructura de directorios
rm -rf templates/\{landing,components\}/
mkdir -p templates/landing
mkdir -p templates/components

# Crear template básico temporal
cat > templates/landing/index.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ config.nombre_empresa }} - {{ config.slogan }}</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            border-radius: 12px;
            margin-bottom: 40px;
        }
        .services {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 15px;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            background: #667eea;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>{{ config.hero_titulo_principal }} <span style="color: #ffd700;">{{ config.hero_titulo_acento }}</span></h1>
        <p style="font-size: 1.2em; margin-top: 20px;">{{ config.hero_subtitulo }}</p>

        <div style="display: flex; gap: 40px; margin-top: 30px;">
            <div>
                <div style="font-size: 2em; font-weight: bold;">{{ config.metrica_1_valor }}</div>
                <div>{{ config.metrica_1_label }}</div>
            </div>
            <div>
                <div style="font-size: 2em; font-weight: bold;">{{ config.metrica_2_valor }}</div>
                <div>{{ config.metrica_2_label }}</div>
            </div>
            <div>
                <div style="font-size: 2em; font-weight: bold;">{{ config.metrica_3_valor }}</div>
                <div>{{ config.metrica_3_label }}</div>
            </div>
        </div>
    </div>

    <h2 style="margin-bottom: 20px;">Nuestros Servicios</h2>
    <div class="services">
        {% for servicio in servicios %}
        <div class="card">
            <h3>{{ servicio.titulo }}</h3>
            <p>{{ servicio.descripcion_corta }}</p>
            {% if servicio.beneficio_clave %}
            <p style="color: #667eea; font-weight: bold;">✓ {{ servicio.beneficio_clave }}</p>
            {% endif %}
        </div>
        {% endfor %}
    </div>

    {% if testimonios %}
    <h2 style="margin-bottom: 20px;">Testimonios</h2>
    <div class="services">
        {% for testimonio in testimonios %}
        <div class="card">
            <p style="font-style: italic; color: #666;">"{{ testimonio.texto }}"</p>
            <p style="margin-top: 15px; font-weight: bold;">{{ testimonio.nombre_cliente }}</p>
            <p style="color: #888; font-size: 0.9em;">{{ testimonio.cargo }}{% if testimonio.empresa %} - {{ testimonio.empresa }}{% endif %}</p>
            {% if testimonio.resultado_clave %}
            <p style="color: #667eea; font-weight: bold; margin-top: 10px;">📈 {{ testimonio.resultado_clave }}</p>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <div class="card" style="margin-top: 40px;">
        <h2>Contáctanos</h2>
        <form method="post" action="{% url 'landing:contacto_submit' %}">
            {% csrf_token %}

            <div class="form-group">
                {{ form.nombre.label_tag }}
                {{ form.nombre }}
                {% if form.nombre.errors %}
                <p style="color: red; font-size: 0.9em;">{{ form.nombre.errors.0 }}</p>
                {% endif %}
            </div>

            <div class="form-group">
                {{ form.email.label_tag }}
                {{ form.email }}
                {% if form.email.errors %}
                <p style="color: red; font-size: 0.9em;">{{ form.email.errors.0 }}</p>
                {% endif %}
            </div>

            <div class="form-group">
                {{ form.telefono.label_tag }}
                {{ form.telefono }}
            </div>

            <div class="form-group">
                {{ form.empresa.label_tag }}
                {{ form.empresa }}
            </div>

            <div class="form-group">
                {{ form.servicio_interes.label_tag }}
                {{ form.servicio_interes }}
            </div>

            <div class="form-group">
                {{ form.mensaje.label_tag }}
                {{ form.mensaje }}
                {% if form.mensaje.errors %}
                <p style="color: red; font-size: 0.9em;">{{ form.mensaje.errors.0 }}</p>
                {% endif %}
            </div>

            <button type="submit">Enviar Mensaje</button>
        </form>
    </div>

    <footer style="margin-top: 60px; padding: 40px 0; border-top: 2px solid #ddd; text-align: center; color: #666;">
        <p>{{ config.nombre_empresa }} - {{ config.email_contacto }}</p>
        <p>WhatsApp: {{ config.whatsapp_numero }}</p>
    </footer>
</body>
</html>
EOF
```

### Paso 7: Crear template de éxito
```bash
cat > templates/components/contacto_success.html << 'EOF'
<div style="background: #10b981; color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <h3>¡Mensaje Enviado Exitosamente!</h3>
    <p>Gracias {{ lead.nombre }}, te contactaremos pronto.</p>
</div>
EOF
```

### Paso 8: Corregir directorios estáticos
```bash
rm -rf static/\{css,js,img\}/
mkdir -p static/css
mkdir -p static/js
mkdir -p static/img
```

### Paso 9: Ejecutar servidor
```bash
python manage.py runserver
```

### Paso 10: Acceder al sistema
1. **Admin Panel:** http://localhost:8000/admin/
   - Usuario: admin (el que creaste)
   - Configurar el sitio en "Configuración del Sitio"
   - Agregar servicios, testimonios, casos de éxito

2. **Landing Page:** http://localhost:8000/
   - Verás la página pública con el template temporal

---

## OPCIÓN 2: Instalación Completa con PostgreSQL

Si quieres usar PostgreSQL (recomendado para producción):

### Paso 1: Instalar PostgreSQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib python3-dev libpq-dev

# Fedora/RHEL
sudo dnf install postgresql-server postgresql-contrib python3-devel

# Arch Linux
sudo pacman -S postgresql
```

### Paso 2: Configurar PostgreSQL
```bash
# Iniciar servicio
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear base de datos y usuario
sudo -u postgres psql << EOF
CREATE DATABASE smartsolutions;
CREATE USER smartsolutions WITH PASSWORD 'smartsolutions';
ALTER ROLE smartsolutions SET client_encoding TO 'utf8';
ALTER ROLE smartsolutions SET default_transaction_isolation TO 'read committed';
ALTER ROLE smartsolutions SET timezone TO 'America/Caracas';
GRANT ALL PRIVILEGES ON DATABASE smartsolutions TO smartsolutions;
\q
EOF
```

### Paso 3: Instalar dependencias completas
```bash
cd "smartsolutions/"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Paso 4: Configurar .env para PostgreSQL
```bash
cat > .env << 'EOF'
# Django
SECRET_KEY=django-insecure-desarrollo-local-cambiar-en-produccion-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos PostgreSQL
DB_NAME=smartsolutions
DB_USER=smartsolutions
DB_PASSWORD=smartsolutions
DB_HOST=localhost
DB_PORT=5432

# Email (Resend)
RESEND_API_KEY=
DEFAULT_FROM_EMAIL=noreply@smartsolutions.com.ve
CONTACT_EMAIL=tu@email.com

# URL del sitio
SITE_URL=http://localhost:8000
EOF
```

### Paso 5: Ejecutar migraciones y arrancar
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📝 Siguientes Pasos Recomendados

1. **Integrar el diseño real:** Convertir `index3.html` (que tiene Tailwind CSS) en templates Django
2. **Crear archivos estáticos:** Extraer CSS y JS del HTML a archivos separados
3. **Configurar Resend:** Obtener API key en https://resend.com para emails
4. **Agregar contenido:** Usar el admin para crear servicios, testimonios, casos de éxito

---

## ⚠️ Problemas Conocidos

- Las carpetas `templates/{landing,components}/` y `static/{css,js,img}/` tienen nombres literales incorrectos (ya corregidos en esta guía)
- No existen migraciones iniciales (se crean con `makemigrations`)
- Los archivos HTML prototipo están fuera del proyecto Django

---

## 🆘 Solución de Problemas

### Error: "No module named django"
```bash
# Asegúrate de activar el entorno virtual
source venv/bin/activate
pip install -r requirements.txt
```

### Error: PostgreSQL connection failed
```bash
# Usar SQLite temporalmente (ver Opción 1)
# O verificar que PostgreSQL esté corriendo:
sudo systemctl status postgresql
```

### Error: "SECRET_KEY not found"
```bash
# Crear archivo .env (ver pasos anteriores)
cp .env.example .env
# Editar .env con tus valores
```
