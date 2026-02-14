# 📚 Documentación Completa - SmartSolutions Landing Page System

> Sistema profesional de landing pages construido con Django 5.1, diseñado para ser reutilizable y escalable.

---

## 📑 Tabla de Contenidos

1. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
2. [Estructura de Directorios](#estructura-de-directorios)
3. [Sistema de Diseño](#sistema-de-diseño)
4. [Configuración Inicial](#configuración-inicial)
5. [Gestión de Contenido](#gestión-de-contenido)
6. [Creación de Nuevas Landing Pages](#creación-de-nuevas-landing-pages)
7. [Personalización Visual](#personalización-visual)
8. [Formularios y Lead Management](#formularios-y-lead-management)
9. [Deployment](#deployment)
10. [Mantenimiento](#mantenimiento)

---

## 🏗️ Arquitectura del Proyecto

### Stack Tecnológico

```
Backend:
├── Django 5.1.5          # Framework web Python
├── Django REST Framework # APIs (opcional, preparado)
├── Django Unfold         # Admin UI mejorado
├── PostgreSQL/SQLite     # Base de datos
├── Resend API            # Emails transaccionales
└── WhiteNoise            # Servir archivos estáticos

Frontend:
├── Tailwind CSS 3.x      # Framework CSS utility-first
├── Alpine.js 3.x         # JavaScript reactivo ligero
├── HTMX                  # AJAX sin JavaScript
├── Font Awesome 6.x      # Iconos
└── Google Fonts          # Tipografías (Outfit, Inter, JetBrains Mono)
```

### Patrón de Arquitectura

El proyecto sigue una arquitectura **modular y escalable**:

```
smartsolutions/
│
├── apps/                    # Apps Django modulares
│   ├── core/               # Configuración global (Singleton)
│   └── landing/            # Funcionalidad landing pages
│
├── smartsolutions/         # Configuración Django
│   ├── settings.py         # Settings
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # WSGI
│
├── templates/              # Templates HTML
│   ├── base.html          # Template base
│   ├── components/        # Componentes reutilizables
│   └── landing/           # Secciones landing page
│
└── static/                # Archivos estáticos
    ├── css/               # Estilos
    ├── js/                # JavaScript
    └── img/               # Imágenes
```

### Patrón Singleton

La configuración del sitio usa el patrón **Singleton** (`ConfiguracionSitio`), garantizando que solo exista una instancia de configuración global:

```python
# apps/core/models.py
class ConfiguracionSitio(SingletonModel):
    """
    Solo puede existir UNA configuración en la base de datos.
    Gestiona todos los textos, colores, y metadatos del sitio.
    """
    nombre_empresa = models.CharField(max_length=200)
    email_contacto = models.EmailField()
    whatsapp_numero = models.CharField(max_length=20)
    # ... más campos
```

**Ventajas:**
- ✅ Una sola fuente de verdad
- ✅ Fácil de actualizar desde el admin
- ✅ No hay duplicación de datos
- ✅ Cambios en tiempo real

---

## 📂 Estructura de Directorios

### Desglose Completo

```
smartsolutions/
│
├── apps/
│   ├── core/                          # App principal
│   │   ├── models.py                  # ConfiguracionSitio (Singleton)
│   │   ├── admin.py                   # Admin personalizado
│   │   ├── context_processors.py     # Inyecta config en templates
│   │   └── migrations/                # Migraciones DB
│   │
│   └── landing/                       # App landing pages
│       ├── models.py                  # Lead, Servicio, Testimonio, Caso
│       ├── views.py                   # Vistas (index, contacto_submit)
│       ├── forms.py                   # ContactoForm
│       ├── admin.py                   # Admin para leads y contenido
│       ├── urls.py                    # URLs de la landing
│       ├── templatetags/              # Custom template filters
│       │   └── custom_filters.py     # Filtro 'mul' para multiplicación
│       └── migrations/
│
├── templates/
│   ├── base.html                      # Template base (navbar + footer)
│   │
│   ├── components/                    # Componentes reutilizables
│   │   ├── navbar.html               # Navegación principal
│   │   ├── footer.html               # Footer
│   │   ├── whatsapp_button.html      # Botón flotante WhatsApp
│   │   ├── contacto_form.html        # Formulario de contacto
│   │   └── contacto_success.html     # Mensaje de éxito
│   │
│   └── landing/                       # Secciones de la landing
│       ├── index.html                # Template principal (ensambla todo)
│       ├── _hero.html                # Sección Hero
│       ├── _desafio.html             # Sección "El Desafío"
│       ├── _metodologia.html         # Sección "Metodología"
│       ├── _servicios.html           # Sección "Servicios"
│       ├── _testimonios.html         # Sección "Testimonios"
│       ├── _contacto.html            # Sección "Contacto"
│       └── _cita.html                # Sección "Cita" (CTA adicional)
│
├── static/
│   ├── css/
│   │   ├── design-system.css         # Sistema de diseño (500+ líneas)
│   │   └── base.css                  # Estilos adicionales
│   │
│   ├── js/
│   │   └── main.js                   # JavaScript custom (si necesario)
│   │
│   └── img/
│       ├── logo.svg                  # Logo SVG
│       ├── og-image.jpg              # Open Graph image
│       └── favicon.png               # Favicon
│
├── smartsolutions/                    # Configuración Django
│   ├── settings.py                   # Settings principales
│   ├── urls.py                       # URLs principales
│   └── wsgi.py                       # WSGI config
│
├── manage.py                          # CLI Django
├── requirements.txt                   # Dependencias Python
├── .env.example                       # Template variables entorno
├── CLAUDE.md                          # Guía para Claude Code
├── SETUP.md                           # Guía de instalación
└── README.md                          # README principal
```

### Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `apps/core/models.py` | Configuración global (Singleton) |
| `apps/landing/models.py` | Modelos de contenido (Lead, Servicio, etc.) |
| `apps/landing/views.py` | Lógica de vistas |
| `apps/landing/forms.py` | Formulario de contacto |
| `templates/base.html` | Template base con Tailwind config |
| `static/css/design-system.css` | Sistema de diseño completo |
| `apps/core/context_processors.py` | Inyecta `config` en todos los templates |

---

## 🎨 Sistema de Diseño

### Paleta de Colores

```css
/* Azul Primary - Brand Principal */
--brand-blue-50: #F0F7FF;
--brand-blue-600: #0066FF;  /* Color principal */
--brand-blue-900: #001A4D;

/* Verde Accent - Acción/Éxito */
--brand-green-500: #34D399;
--brand-green-600: #10B981;  /* Color principal */

/* Amber - Destacados */
--brand-amber-400: #FBBF24;
--brand-amber-500: #F59E0B;  /* Color principal */

/* Navy - Fondos Oscuros */
--brand-navy-900: #0F172A;
--brand-navy-950: #020617;
```

### Tipografías

```css
/* Display - Títulos y Headlines */
font-family: 'Outfit', sans-serif;
font-weight: 800, 900 (Black, ExtraBold)

/* Body - Texto general */
font-family: 'Inter', sans-serif;
font-weight: 400, 500, 600

/* Mono - Números y código */
font-family: 'JetBrains Mono', monospace;
font-weight: 500, 600, 700
```

### Espaciado (Escala 8px)

```css
--spacing-1: 8px;
--spacing-2: 16px;
--spacing-3: 24px;
--spacing-4: 32px;
--spacing-6: 48px;
--spacing-8: 64px;
```

### Shadows

```css
/* Primary - Para elementos blue */
box-shadow: 0 10px 40px -10px rgba(0, 102, 255, 0.25);

/* Accent - Para elementos green */
box-shadow: 0 10px 40px -10px rgba(16, 185, 129, 0.25);
```

### Efectos Glassmorphism

```css
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-card-premium {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(30px) saturate(200%);
    border: 1px solid rgba(255, 255, 255, 0.15);
}
```

### Animaciones Disponibles

```css
/* Fade In */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Slide In from Bottom */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(40px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Scale In */
@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Pulse Glow */
@keyframes pulse-glow {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Float */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Shimmer */
@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}
```

### Patrones de Fondo

```css
/* Dots Pattern */
.pattern-subtle-dots {
    background-image: radial-gradient(circle, rgba(0,0,0,0.1) 1px, transparent 1px);
    background-size: 20px 20px;
}

/* Grid Pattern */
.pattern-subtle-grid {
    background-image:
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 40px 40px;
}

/* Hero Pattern Grid (for dark backgrounds) */
.hero-pattern-grid {
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
}
```

---

## ⚙️ Configuración Inicial

### 1. Instalación del Entorno

```bash
# Clonar o descargar el proyecto
cd "Smart Solutions/smartsolutions"

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Django
SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL en producción)
DATABASE_URL=postgresql://usuario:password@localhost:5432/smartsolutions_db

# Email (Resend API)
RESEND_API_KEY=re_tu_api_key_aqui
EMAIL_FROM=noreply@tudominio.com
EMAIL_TO_ADMIN=admin@tudominio.com

# WhatsApp
WHATSAPP_NUMBER=+584121691851

# URLs (para Open Graph y sitemap)
SITE_URL=https://tudominio.com
```

### 3. Inicializar Base de Datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 4. Configurar la Instancia Singleton

```bash
# Abrir shell de Django
python manage.py shell
```

```python
from apps.core.models import ConfiguracionSitio

# Crear la configuración del sitio (solo una vez)
config = ConfiguracionSitio.objects.create(
    nombre_empresa="SmartSolutions VE",
    email_contacto="contacto@smartsolutions.ve",
    whatsapp_numero="+58 412 169 1851",
    descripcion_corta="Transformamos PYMEs venezolanas con consultoría estratégica y tecnología.",

    # SEO
    meta_titulo="SmartSolutions VE | Consultoría Estratégica en Valencia",
    meta_descripcion="Transformamos la incertidumbre operativa en claridad estratégica. +50 PYMEs transformadas.",

    # Hero Section
    hero_titulo_principal="Transforma el Caos",
    hero_titulo_acento="en Claridad",
    hero_subtitulo="Consultoría estratégica y tecnológica para PYMEs venezolanas que quieren escalar con control.",

    # Métricas
    metrica_1_label="Incremento en Eficiencia",
    metrica_1_valor="+50",
    metrica_2_label="Aumento en Rentabilidad",
    metrica_2_valor="+200",
    metrica_3_label="Días de ROI",
    metrica_3_valor="<90",

    # Redes sociales
    linkedin_url="https://linkedin.com/company/smartsolutions-ve",
    instagram_url="https://instagram.com/smartsolutions.ve",
)
```

### 5. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

Abrir navegador en: `http://localhost:8000`

---

## 📝 Gestión de Contenido

### Panel de Administración

Acceder a: `http://localhost:8000/admin`

### Configuración Global (Singleton)

**Ubicación:** Admin → Core → Configuración Sitio

**Campos Principales:**

```
Información Básica:
├── Nombre Empresa
├── Email Contacto
├── WhatsApp Número
├── Descripción Corta
└── Descripción Larga

SEO y Metadatos:
├── Meta Título
├── Meta Descripción
├── Meta Keywords
└── OG Image

Hero Section:
├── Título Principal
├── Título Acento
├── Subtítulo
└── 3 Métricas (Label + Valor)

Redes Sociales:
├── LinkedIn URL
├── Instagram URL
├── Twitter URL
└── Facebook URL

Configuración Técnica:
├── Resend API Key
├── Email From
└── Email To Admin
```

### Servicios

**Ubicación:** Admin → Landing → Servicios

**Campos:**

```python
titulo = "Business Intelligence & Dashboards"
descripcion_corta = "Convertimos tus datos en decisiones estratégicas con dashboards en tiempo real."
descripcion_larga = "Implementación completa de sistemas BI..."
beneficio_clave = "Decisiones basadas en data en tiempo real"
icono = "chart-bar"  # Font Awesome icon name
orden = 1  # Orden de visualización
activo = True  # Mostrar/ocultar
```

**Íconos Disponibles:**
- `chart-bar` - Business Intelligence
- `cog` - Automatización
- `mobile-screen` - Apps Móviles
- `database` - Gestión de Datos
- `bolt` - Optimización
- `chart-line` - Analytics
- `cube` - Desarrollo Custom
- `shield-halved` - Seguridad

### Testimonios

**Ubicación:** Admin → Landing → Testimonios

```python
nombre_cliente = "Carlos Rodríguez"
cargo = "CEO"
empresa = "Distribuidora Los Andes"
texto = "SmartSolutions transformó completamente nuestra operación..."
resultado_clave = "+150% en eficiencia operativa"
foto = imagen_perfil.jpg  # Opcional
orden = 1
activo = True
```

### Casos de Éxito

**Ubicación:** Admin → Landing → Casos de Éxito

```python
titulo = "Automatización de Inventario"
empresa = "Ferretería Central"
sector = "Retail"
descripcion = "Implementamos un sistema automático..."
imagen = case_study_ferreteria.jpg  # Opcional
metricas = [
    {"valor": "+80%", "label": "Eficiencia"},
    {"valor": "-40%", "label": "Errores"}
]
orden = 1
activo = True
```

### Leads (Contactos)

**Ubicación:** Admin → Landing → Leads

Los formularios de contacto se guardan automáticamente aquí.

**Campos:**
```python
nombre = "Juan Pérez"
email = "juan@empresa.com"
telefono = "+58 412 123 4567"  # Opcional
empresa = "Mi Empresa CA"  # Opcional
servicio_interes = "Business Intelligence"  # Opcional
mensaje = "Me interesa conocer más sobre..."
fecha_creacion = auto
estado = "nuevo"  # nuevo, contactado, calificado, cerrado
```

**Estados de Lead:**
- `nuevo` - Recién llegado
- `contactado` - Ya se contactó
- `calificado` - Lead calificado
- `cerrado` - Cerrado (ganado o perdido)

---

## 🆕 Creación de Nuevas Landing Pages

### Método 1: Duplicar Landing Existente

#### Paso 1: Crear Nueva App Django

```bash
python manage.py startapp nueva_landing
mv nueva_landing apps/
```

#### Paso 2: Copiar Estructura de `landing/`

```bash
# Copiar estructura base
cp -r apps/landing/* apps/nueva_landing/

# Actualizar imports en todos los archivos
# Cambiar 'apps.landing' por 'apps.nueva_landing'
```

#### Paso 3: Registrar Nueva App

En `smartsolutions/settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'apps.core',
    'apps.landing',
    'apps.nueva_landing',  # Nueva app
]
```

#### Paso 4: Crear URLs

En `apps/nueva_landing/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'nueva_landing'

urlpatterns = [
    path('', views.index, name='index'),
    path('contacto/submit/', views.contacto_submit, name='contacto_submit'),
]
```

En `smartsolutions/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.landing.urls')),
    path('nueva/', include('apps.nueva_landing.urls')),  # Nueva landing
]
```

#### Paso 5: Personalizar Templates

```bash
# Crear directorio de templates
mkdir -p templates/nueva_landing

# Copiar templates base
cp templates/landing/* templates/nueva_landing/

# Personalizar contenido según la nueva landing
```

#### Paso 6: Migrar Base de Datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### Método 2: Landing Page con Misma App (Multi-Tenant)

Si quieres múltiples landing pages usando la misma app pero con diferentes configuraciones:

#### Paso 1: Extender Modelo Singleton

En `apps/core/models.py`:

```python
class ConfiguracionLanding(models.Model):
    """Múltiples configuraciones para diferentes landing pages"""

    slug = models.SlugField(unique=True)  # ej: "servicios-tech", "consultoria-legal"
    nombre = models.CharField(max_length=200)
    activa = models.BooleanField(default=True)

    # Mismos campos que ConfiguracionSitio
    email_contacto = models.EmailField()
    whatsapp_numero = models.CharField(max_length=20)
    # ... etc

    class Meta:
        verbose_name_plural = "Configuraciones Landing"
```

#### Paso 2: Crear Vista Dinámica

En `apps/landing/views.py`:

```python
def landing_dinamica(request, slug):
    """Vista que carga diferentes configuraciones según el slug"""

    config_landing = get_object_or_404(ConfiguracionLanding, slug=slug, activa=True)

    context = {
        'config': config_landing,
        'servicios': Servicio.objects.filter(activo=True, landing=config_landing),
        'testimonios': Testimonio.objects.filter(activo=True, landing=config_landing),
    }

    return render(request, 'landing/index.html', context)
```

#### Paso 3: Configurar URLs

```python
urlpatterns = [
    path('<slug:slug>/', views.landing_dinamica, name='landing_dinamica'),
]
```

**Resultado:**
- `/servicios-tech/` → Landing de Servicios Tecnológicos
- `/consultoria-legal/` → Landing de Consultoría Legal
- `/marketing-digital/` → Landing de Marketing Digital

### Método 3: Landing Page Estática (HTML + Tailwind)

Para landing pages sin backend, solo frontend:

#### Paso 1: Crear Archivo HTML

```html
<!-- templates/landings/servicios-tech.html -->
{% extends "base.html" %}
{% load static %}

{% block content %}
<section class="hero">
    <!-- Tu contenido personalizado aquí -->
</section>
{% endblock %}
```

#### Paso 2: Crear Vista Simple

```python
def servicios_tech(request):
    return render(request, 'landings/servicios-tech.html')
```

#### Paso 3: Agregar URL

```python
path('servicios-tech/', views.servicios_tech, name='servicios_tech'),
```

---

## 🎨 Personalización Visual

### Cambiar Colores de Marca

#### Opción 1: Modificar Tailwind Config en `base.html`

```html
<script>
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    'brand-blue': {
                        600: '#TU_NUEVO_COLOR',  // Cambiar aquí
                    },
                    // ... etc
                }
            }
        }
    }
</script>
```

#### Opción 2: Modificar `design-system.css`

```css
:root {
    /* Colores Primary */
    --brand-blue-600: #TU_NUEVO_COLOR;
    --brand-green-600: #TU_NUEVO_COLOR;
    --brand-amber-500: #TU_NUEVO_COLOR;
}
```

### Cambiar Tipografías

En `base.html`, actualizar Google Fonts:

```html
<!-- Cambiar estas líneas -->
<link href="https://fonts.googleapis.com/css2?family=TU_FUENTE_DISPLAY&family=TU_FUENTE_BODY&display=swap" rel="stylesheet">

<script>
    tailwind.config = {
        theme: {
            extend: {
                fontFamily: {
                    'display': ['TU_FUENTE_DISPLAY', 'sans-serif'],
                    'body': ['TU_FUENTE_BODY', 'sans-serif'],
                }
            }
        }
    }
</script>
```

### Modificar Secciones

Todas las secciones están en archivos separados en `templates/landing/`:

```
_hero.html          → Sección Hero
_desafio.html       → El Desafío
_metodologia.html   → Metodología
_servicios.html     → Servicios
_testimonios.html   → Testimonios
_contacto.html      → Formulario de Contacto
```

**Para modificar una sección:**

1. Abrir el archivo correspondiente
2. Editar el HTML/Tailwind
3. Guardar y refrescar navegador
4. Django recarga automáticamente en modo desarrollo

### Agregar Nueva Sección

#### Paso 1: Crear Template

```html
<!-- templates/landing/_nueva_seccion.html -->
{% load static %}

<section id="nueva-seccion" class="py-32 px-6 bg-white">
    <div class="max-w-7xl mx-auto">
        <h2 class="text-5xl font-black mb-8 font-display">
            Nueva Sección
        </h2>
        <!-- Tu contenido aquí -->
    </div>
</section>
```

#### Paso 2: Incluir en `index.html`

```html
<!-- templates/landing/index.html -->
{% include 'landing/_hero.html' %}
{% include 'landing/_desafio.html' %}
{% include 'landing/_nueva_seccion.html' %}  <!-- Nueva sección -->
{% include 'landing/_servicios.html' %}
```

#### Paso 3: Agregar Link en Navbar

```html
<!-- templates/components/navbar.html -->
<a href="#nueva-seccion" class="nav-link">Nueva Sección</a>
```

---

## 📧 Formularios y Lead Management

### Flujo de Contacto

1. **Usuario llena formulario** en `#contacto`
2. **HTMX envía POST** a `/contacto/submit/`
3. **Django valida datos** con `ContactoForm`
4. **Se crea Lead** en base de datos
5. **Se envía email** vía Resend API
6. **Respuesta HTMX** reemplaza formulario con mensaje de éxito

### Configurar Resend API

#### Paso 1: Crear Cuenta en Resend

1. Ir a [resend.com](https://resend.com)
2. Crear cuenta gratuita (3000 emails/mes)
3. Verificar dominio
4. Obtener API Key

#### Paso 2: Configurar en `.env`

```env
RESEND_API_KEY=re_tu_api_key
EMAIL_FROM=noreply@tudominio.com
EMAIL_TO_ADMIN=admin@tudominio.com
```

#### Paso 3: Verificar en Admin

Admin → Core → Configuración Sitio → Sección "Configuración Email"

### Personalizar Email de Notificación

En `apps/landing/views.py`:

```python
def enviar_email_notificacion(lead):
    """Personaliza el email enviado al admin"""

    html_content = f"""
    <html>
        <body style="font-family: sans-serif; padding: 20px;">
            <h2 style="color: #0066FF;">🎉 Nuevo Lead en SmartSolutions</h2>

            <div style="background: #f5f5f5; padding: 20px; border-radius: 8px;">
                <p><strong>Nombre:</strong> {lead.nombre}</p>
                <p><strong>Email:</strong> {lead.email}</p>
                <p><strong>Teléfono:</strong> {lead.telefono or 'No proporcionado'}</p>
                <p><strong>Empresa:</strong> {lead.empresa or 'No proporcionado'}</p>
                <p><strong>Servicio de Interés:</strong> {lead.servicio_interes or 'No especificado'}</p>
                <p><strong>Mensaje:</strong></p>
                <p>{lead.mensaje}</p>
            </div>

            <p style="margin-top: 20px;">
                <a href="{settings.SITE_URL}/admin/landing/lead/{lead.id}/change/"
                   style="background: #0066FF; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">
                    Ver en Admin
                </a>
            </p>
        </body>
    </html>
    """

    # Enviar con Resend
    resend.Emails.send({
        "from": settings.EMAIL_FROM,
        "to": settings.EMAIL_TO_ADMIN,
        "subject": f"Nuevo Lead: {lead.nombre}",
        "html": html_content
    })
```

### Agregar Auto-respuesta al Cliente

```python
def enviar_autorespuesta(lead):
    """Email automático de confirmación al cliente"""

    html_content = f"""
    <html>
        <body>
            <h2>¡Gracias por contactarnos, {lead.nombre}! 🎉</h2>

            <p>Hemos recibido tu mensaje y nos pondremos en contacto contigo en las próximas 24 horas.</p>

            <p><strong>Resumen de tu consulta:</strong></p>
            <p>{lead.mensaje}</p>

            <p>Mientras tanto, síguenos en redes sociales:</p>
            <p>
                LinkedIn: https://linkedin.com/company/smartsolutions-ve<br>
                Instagram: @smartsolutions.ve
            </p>

            <p>Saludos,<br>Equipo SmartSolutions</p>
        </body>
    </html>
    """

    resend.Emails.send({
        "from": settings.EMAIL_FROM,
        "to": lead.email,
        "subject": "¡Gracias por contactarnos!",
        "html": html_content
    })
```

Llamar en `contacto_submit`:

```python
enviar_email_notificacion(lead)
enviar_autorespuesta(lead)  # Agregar esta línea
```

### Pipeline de Leads en Admin

**Estados sugeridos:**

```python
ESTADO_CHOICES = [
    ('nuevo', '🆕 Nuevo'),
    ('contactado', '📞 Contactado'),
    ('reunion_agendada', '📅 Reunión Agendada'),
    ('propuesta_enviada', '📄 Propuesta Enviada'),
    ('negociacion', '💬 En Negociación'),
    ('ganado', '✅ Ganado'),
    ('perdido', '❌ Perdido'),
]
```

**Agregar al modelo Lead:**

```python
estado = models.CharField(
    max_length=20,
    choices=ESTADO_CHOICES,
    default='nuevo'
)
notas = models.TextField(blank=True)  # Notas internas
fecha_ultimo_contacto = models.DateTimeField(null=True, blank=True)
```

---

## 🚀 Deployment

### Preparación para Producción

#### 1. Actualizar `settings.py`

```python
# Seguridad
DEBUG = False
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']
SECRET_KEY = os.getenv('SECRET_KEY')

# Base de datos
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

# Archivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Seguridad adicional
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

#### 2. Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

#### 3. Configurar Gunicorn

Crear `Procfile`:

```
web: gunicorn smartsolutions.wsgi --log-file -
```

### Deployment en Heroku

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Crear app
heroku create smartsolutions-ve

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Configurar variables de entorno
heroku config:set SECRET_KEY=tu-secret-key
heroku config:set RESEND_API_KEY=tu-resend-key
heroku config:set EMAIL_FROM=noreply@tudominio.com
heroku config:set EMAIL_TO_ADMIN=admin@tudominio.com

# Deploy
git push heroku main

# Migrar base de datos
heroku run python manage.py migrate

# Crear superusuario
heroku run python manage.py createsuperuser
```

### Deployment en Railway

1. Ir a [railway.app](https://railway.app)
2. Conectar repositorio GitHub
3. Agregar PostgreSQL
4. Configurar variables de entorno
5. Deploy automático

### Deployment en VPS (DigitalOcean, Linode, etc.)

#### Stack Recomendado:

```
Nginx → Gunicorn → Django → PostgreSQL
```

#### Pasos:

1. **Servidor**: Ubuntu 22.04 LTS
2. **Python**: 3.11+
3. **Web Server**: Nginx
4. **WSGI**: Gunicorn
5. **Database**: PostgreSQL 15
6. **Process Manager**: Systemd
7. **SSL**: Let's Encrypt (Certbot)

Guía completa en: [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)

---

## 🔧 Mantenimiento

### Actualizar Dependencias

```bash
# Ver paquetes desactualizados
pip list --outdated

# Actualizar paquete específico
pip install --upgrade nombre-paquete

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### Backup de Base de Datos

#### PostgreSQL:

```bash
# Backup
pg_dump dbname > backup.sql

# Restore
psql dbname < backup.sql
```

#### Django:

```bash
# Dump datos
python manage.py dumpdata > backup.json

# Load datos
python manage.py loaddata backup.json
```

### Logs y Monitoreo

#### Django Logs:

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

#### Monitoreo Recomendado:

- **Sentry** - Error tracking
- **Google Analytics** - Web analytics
- **Hotjar** - Heatmaps y grabaciones
- **New Relic** - Application monitoring

### Performance Optimization

#### 1. Cache

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# En views.py
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache 15 minutos
def index(request):
    # ...
```

#### 2. Database Queries

```python
# Usar select_related para ForeignKey
servicios = Servicio.objects.select_related('categoria').all()

# Usar prefetch_related para ManyToMany
servicios = Servicio.objects.prefetch_related('tags').all()
```

#### 3. Comprimir Archivos Estáticos

```bash
# Con WhiteNoise (ya configurado)
python manage.py collectstatic --noinput

# Minificar CSS/JS manualmente
npm install -g csso-cli
csso style.css -o style.min.css
```

### Seguridad

#### Checklist:

- [ ] `DEBUG = False` en producción
- [ ] `SECRET_KEY` en variable de entorno
- [ ] HTTPS configurado (SSL/TLS)
- [ ] Firewall configurado
- [ ] PostgreSQL con password fuerte
- [ ] Backup automático configurado
- [ ] Actualizar dependencias regularmente
- [ ] Rate limiting en formularios
- [ ] CSRF protection activo
- [ ] XSS protection activo

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Alpine.js Documentation](https://alpinejs.dev/)
- [HTMX Documentation](https://htmx.org/docs/)

### Comunidad

- [Django Forum](https://forum.djangoproject.com/)
- [Stack Overflow - Django](https://stackoverflow.com/questions/tagged/django)
- [Reddit r/django](https://reddit.com/r/django)

### Herramientas Útiles

- **Django Debug Toolbar** - Debug en desarrollo
- **Django Extensions** - Comandos útiles
- **Black** - Python code formatter
- **Flake8** - Linter Python
- **Pre-commit** - Git hooks

---

## 🎓 Conclusión

Este sistema está diseñado para ser:

✅ **Fácil de usar** - Admin intuitivo para gestionar contenido
✅ **Reutilizable** - Crear nuevas landing pages en minutos
✅ **Escalable** - Arquitectura modular y extensible
✅ **Profesional** - Diseño premium y código limpio
✅ **Mantenible** - Código bien documentado

Para cualquier duda o mejora, consultar `CLAUDE.md` o `RECOMMENDATIONS.md`.

---

**Última actualización:** Febrero 2026
**Versión:** 1.0.0
**Autor:** SmartSolutions VE
