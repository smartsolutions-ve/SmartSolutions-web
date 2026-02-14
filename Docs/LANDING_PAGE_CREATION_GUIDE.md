# 🎨 Guía Práctica: Crear Nuevas Landing Pages

> Tutorial paso a paso para crear landing pages profesionales usando SmartSolutions

---

## 📋 Tabla de Contenidos

1. [Preparación](#preparación)
2. [Método 1: Landing Simple (30 minutos)](#método-1-landing-simple)
3. [Método 2: Landing Personalizada (2 horas)](#método-2-landing-personalizada)
4. [Método 3: Multi-Landing SaaS (4+ horas)](#método-3-multi-landing-saas)
5. [Checklist de Lanzamiento](#checklist-de-lanzamiento)
6. [Casos de Uso Comunes](#casos-de-uso-comunes)

---

## 🎯 Preparación

### Antes de Empezar

**Necesitarás:**

- [ ] Contenido de la landing (textos, imágenes)
- [ ] Logo de la empresa (SVG preferiblemente)
- [ ] Paleta de colores (2-3 colores principales)
- [ ] Email de contacto
- [ ] Número de WhatsApp

**Herramientas útiles:**

- **Coolors.co** - Generar paleta de colores
- **Unsplash** - Imágenes gratuitas de alta calidad
- **Canva** - Crear gráficos simples
- **Google Fonts** - Elegir tipografías

---

## 🚀 Método 1: Landing Simple (30 minutos)

> Usar la estructura existente cambiando solo el contenido vía Admin.

### Paso 1: Acceder al Admin (2 min)

```
1. Ir a http://localhost:8000/admin
2. Login con superusuario
3. Ir a Core → Configuración Sitio
```

### Paso 2: Actualizar Información Básica (5 min)

```python
# En Admin → Configuración Sitio

Nombre Empresa: "TuEmpresa CA"
Email Contacto: "contacto@tuempresa.com"
WhatsApp Número: "+58 412 XXX XXXX"

Descripción Corta:
"Transformamos negocios con tecnología y estrategia"
```

### Paso 3: Personalizar Hero Section (5 min)

```python
# Títulos
Hero Título Principal: "Crea Tu Éxito"
Hero Título Acento: "Con Nosotros"
Hero Subtítulo: "Consultoría profesional para empresas que quieren crecer"

# Métricas
Métrica 1 Label: "Clientes Satisfechos"
Métrica 1 Valor: "+100"

Métrica 2 Label: "Proyectos Completados"
Métrica 2 Valor: "+250"

Métrica 3 Label: "Años de Experiencia"
Métrica 3 Valor: "10+"
```

### Paso 4: Agregar Servicios (10 min)

```
Admin → Landing → Servicios → Agregar Servicio

Servicio 1:
├── Título: "Consultoría Estratégica"
├── Descripción Corta: "Te ayudamos a definir tu estrategia de crecimiento..."
├── Beneficio Clave: "ROI medible en 90 días"
├── Ícono: "chart-line"
├── Orden: 1
└── Activo: ✓

Servicio 2:
├── Título: "Transformación Digital"
├── Descripción Corta: "Moderniza tus procesos con tecnología..."
├── Beneficio Clave: "+150% en eficiencia"
├── Ícono: "bolt"
├── Orden: 2
└── Activo: ✓

Servicio 3:
├── Título: "Business Intelligence"
├── Descripción Corta: "Toma decisiones basadas en datos reales..."
├── Beneficio Clave: "Decisiones en tiempo real"
├── Ícono: "chart-bar"
├── Orden: 3
└── Activo: ✓
```

### Paso 5: Agregar Testimonios (5 min)

```
Admin → Landing → Testimonios → Agregar Testimonio

Testimonio 1:
├── Nombre Cliente: "María González"
├── Cargo: "CEO"
├── Empresa: "TechCorp"
├── Texto: "Excelente trabajo, superaron nuestras expectativas..."
├── Resultado Clave: "+80% en ventas"
├── Foto: (opcional)
├── Orden: 1
└── Activo: ✓
```

### Paso 6: Configurar SEO (3 min)

```python
Meta Título: "TuEmpresa - Consultoría Profesional en Valencia"
Meta Descripción: "Transformamos empresas con estrategia y tecnología. +100 clientes satisfechos."
Meta Keywords: "consultoría, venezuela, transformación digital"
```

### Resultado

✅ Landing page funcional en 30 minutos
✅ Contenido dinámico desde Admin
✅ Formulario de contacto operativo
✅ SEO básico configurado

**Siguiente:** Cambiar colores (si necesario)

---

## 🎨 Método 2: Landing Personalizada (2 horas)

> Personalizar diseño visual: colores, tipografías, secciones.

### Paso 1: Definir Identidad Visual (15 min)

**1.1 Elegir Colores Primarios**

Ir a [Coolors.co](https://coolors.co) y generar paleta:

```
Ejemplo para una empresa tech:
├── Primary: #2563EB (Azul)
├── Secondary: #10B981 (Verde)
├── Accent: #F59E0B (Naranja)
└── Dark: #1E293B (Navy)
```

**1.2 Elegir Tipografías**

Ir a [Google Fonts](https://fonts.google.com):

```
Display (Títulos): Poppins (Bold/ExtraBold)
Body (Texto): Inter (Regular/Medium)
```

### Paso 2: Actualizar Colores (20 min)

**2.1 En `base.html` (línea 40):**

```html
<script>
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    'brand-blue': {
                        600: '#2563EB',  // ← TU COLOR AQUÍ
                    },
                    'brand-green': {
                        600: '#10B981',  // ← TU COLOR AQUÍ
                    },
                    'brand-amber': {
                        500: '#F59E0B',  // ← TU COLOR AQUÍ
                    },
                }
            }
        }
    }
</script>
```

**2.2 En `design-system.css` (línea 5):**

```css
:root {
    --brand-blue-600: #2563EB;    /* TU COLOR */
    --brand-green-600: #10B981;   /* TU COLOR */
    --brand-amber-500: #F59E0B;   /* TU COLOR */
}
```

### Paso 3: Actualizar Tipografías (15 min)

**3.1 En `base.html` (línea 36):**

```html
<!-- Cambiar Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

**3.2 En Tailwind Config (línea 97):**

```javascript
fontFamily: {
    'display': ['Poppins', 'sans-serif'],  // TU FUENTE
    'body': ['Inter', 'sans-serif'],       // TU FUENTE
}
```

### Paso 4: Personalizar Logo (15 min)

**Opción A: Logo como Imagen**

```html
<!-- En navbar.html, línea 14 -->
<a href="{% url 'landing:index' %}" class="flex items-center gap-3">
    <img src="{% static 'img/logo.svg' %}"
         alt="Logo"
         class="h-10 w-auto">
    <span class="text-xl font-black text-neutral-900 font-display">
        TuEmpresa
    </span>
</a>
```

**Opción B: Logo SVG Inline (Personalizar)**

Editar el SVG en `navbar.html` líneas 18-41 con tu diseño.

### Paso 5: Modificar Secciones (40 min)

**5.1 Ocultar/Mostrar Secciones**

En `templates/landing/index.html`:

```html
{% include 'landing/_hero.html' %}           ✓ Mantener
{% include 'landing/_desafio.html' %}        ✓ Mantener
{% include 'landing/_metodologia.html' %}    ✗ Comentar si no aplica
{% include 'landing/_servicios.html' %}      ✓ Mantener
{% include 'landing/_testimonios.html' %}    ✓ Mantener
{% include 'landing/_cita.html' %}           ✗ Opcional
{% include 'landing/_contacto.html' %}       ✓ Mantener
```

**5.2 Personalizar Textos de Sección**

Editar directamente los archivos:

```
templates/landing/_desafio.html
├── Línea 26: "El Desafío Actual"          → Cambiar título
├── Línea 34: "En el entorno empresarial..." → Cambiar descripción
└── Líneas 49-107: Modificar problemas listados

templates/landing/_metodologia.html
├── Línea 31: "Nuestro Proceso"            → Cambiar badge
├── Línea 35: "Metodología de Acción"     → Cambiar título
└── Editar los 4 pasos según tu metodología
```

**5.3 Agregar Nueva Sección (Opcional)**

```html
<!-- templates/landing/_nueva_seccion.html -->
{% load static %}

<section id="nueva-seccion" class="relative py-32 px-6 bg-white">
    <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
            <h2 class="text-5xl font-black mb-6 font-display">
                Tu Nuevo Título
            </h2>
            <p class="text-xl text-neutral-600 font-body">
                Tu descripción aquí
            </p>
        </div>

        <!-- Tu contenido aquí -->
        <div class="grid grid-cols-3 gap-8">
            <!-- Cards, imágenes, etc. -->
        </div>
    </div>
</section>
```

Incluir en `index.html`:

```html
{% include 'landing/_nueva_seccion.html' %}
```

### Paso 6: Actualizar Imágenes (20 min)

**6.1 Descargar Imágenes de Stock**

- [Unsplash](https://unsplash.com) - Gratis, alta calidad
- [Pexels](https://pexels.com) - Gratis
- [Freepik](https://freepik.com) - Requiere atribución

**6.2 Optimizar Imágenes**

```bash
# Redimensionar y optimizar
pip install pillow

python
>>> from PIL import Image
>>> img = Image.open('imagen.jpg')
>>> img.thumbnail((1920, 1080))
>>> img.save('imagen_optimizada.jpg', quality=85, optimize=True)
```

**6.3 Colocar en Static**

```bash
mv imagen_optimizada.jpg static/img/
```

**6.4 Usar en Template**

```html
<img src="{% static 'img/imagen_optimizada.jpg' %}"
     alt="Descripción"
     loading="lazy">
```

### Resultado

✅ Diseño visual personalizado
✅ Colores de marca aplicados
✅ Tipografías profesionales
✅ Logo personalizado
✅ Secciones ajustadas al negocio
✅ Imágenes optimizadas

---

## 🏢 Método 3: Multi-Landing SaaS (4+ horas)

> Sistema para gestionar múltiples landing pages (multi-tenant).

### Arquitectura

```
smartsolutions.com/              → Landing principal
smartsolutions.com/tech/         → Landing tech
smartsolutions.com/legal/        → Landing legal
smartsolutions.com/marketing/    → Landing marketing
```

### Paso 1: Crear Modelo Multi-Landing (30 min)

**1.1 Crear modelo:**

```python
# apps/core/models.py
class ConfiguracionLanding(models.Model):
    """Múltiples configuraciones para diferentes landings"""

    # Identificación
    slug = models.SlugField(unique=True, help_text="URL: /slug/")
    nombre = models.CharField(max_length=200)
    activa = models.BooleanField(default=True)

    # Información Básica
    email_contacto = models.EmailField()
    whatsapp_numero = models.CharField(max_length=20)
    descripcion_corta = models.TextField()

    # Hero Section
    hero_titulo_principal = models.CharField(max_length=200)
    hero_titulo_acento = models.CharField(max_length=100)
    hero_subtitulo = models.TextField()

    # Métricas
    metrica_1_label = models.CharField(max_length=100)
    metrica_1_valor = models.CharField(max_length=20)
    metrica_2_label = models.CharField(max_length=100)
    metrica_2_valor = models.CharField(max_length=20)
    metrica_3_label = models.CharField(max_length=100)
    metrica_3_valor = models.CharField(max_length=20)

    # SEO
    meta_titulo = models.CharField(max_length=60)
    meta_descripcion = models.CharField(max_length=160)

    # Colores (opcional)
    color_primary = models.CharField(max_length=7, default='#0066FF')
    color_secondary = models.CharField(max_length=7, default='#10B981')

    # Redes sociales
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Configuración Landing"
        verbose_name_plural = "Configuraciones Landing"

    def __str__(self):
        return f"{self.nombre} (/{self.slug}/)"
```

**1.2 Extender modelos relacionados:**

```python
# apps/landing/models.py
class Servicio(models.Model):
    # Agregar campo para asociar a landing específica
    landing = models.ForeignKey(
        'core.ConfiguracionLanding',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Dejar vacío para landing principal"
    )
    # ... resto de campos
```

```python
# Mismo para Testimonio, Caso, etc.
class Testimonio(models.Model):
    landing = models.ForeignKey('core.ConfiguracionLanding', ...)
    # ...

class Caso(models.Model):
    landing = models.ForeignKey('core.ConfiguracionLanding', ...)
    # ...
```

**1.3 Migrar:**

```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 2: Crear Vista Dinámica (20 min)

```python
# apps/landing/views.py
def landing_dinamica(request, slug=None):
    """Vista que sirve diferentes landing pages según el slug"""

    if slug:
        # Cargar configuración específica
        config_landing = get_object_or_404(
            ConfiguracionLanding,
            slug=slug,
            activa=True
        )

        # Filtrar contenido por landing
        servicios = Servicio.objects.filter(
            activo=True,
            landing=config_landing
        ).order_by('orden')

        testimonios = Testimonio.objects.filter(
            activo=True,
            landing=config_landing
        ).order_by('orden')

        casos = Caso.objects.filter(
            activo=True,
            landing=config_landing
        ).order_by('orden')

    else:
        # Landing principal (usa ConfiguracionSitio singleton)
        config_landing = ConfiguracionSitio.objects.first()

        servicios = Servicio.objects.filter(
            activo=True,
            landing__isnull=True  # Solo servicios sin landing específica
        ).order_by('orden')

        testimonios = Testimonio.objects.filter(
            activo=True,
            landing__isnull=True
        ).order_by('orden')

        casos = Caso.objects.filter(
            activo=True,
            landing__isnull=True
        ).order_by('orden')

    context = {
        'config': config_landing,
        'servicios': servicios,
        'testimonios': testimonios,
        'casos': casos,
    }

    return render(request, 'landing/index.html', context)
```

**Configurar URLs:**

```python
# apps/landing/urls.py
urlpatterns = [
    path('', views.landing_dinamica, name='index'),  # Landing principal
    path('<slug:slug>/', views.landing_dinamica, name='landing_dinamica'),  # Otras landings
    path('contacto/submit/', views.contacto_submit, name='contacto_submit'),
]
```

### Paso 3: Crear Landings desde Admin (15 min cada una)

**3.1 Landing Tech:**

```
Admin → Core → Configuraciones Landing → Agregar

Slug: "tech"                            → URL: /tech/
Nombre: "SmartSolutions Tech"
Activa: ✓

Email Contacto: "tech@smartsolutions.ve"
WhatsApp: "+58 412 XXX XXXX"

Hero Título Principal: "Impulsa tu Negocio"
Hero Título Acento: "Con Tecnología"
Hero Subtítulo: "Desarrollo de software a medida para empresas..."

Métrica 1: "Apps Desarrolladas" / "+50"
Métrica 2: "Clientes Tech" / "+30"
Métrica 3: "Uptime" / "99.9%"

Meta Título: "SmartSolutions Tech - Desarrollo de Software"
Meta Descripción: "Desarrollamos apps móviles, web y sistemas..."

Color Primary: #6366F1 (Indigo)
Color Secondary: #8B5CF6 (Purple)
```

**3.2 Agregar Servicios para Tech:**

```
Admin → Landing → Servicios → Agregar

Landing: "SmartSolutions Tech (tech)"  ← Seleccionar
Título: "Desarrollo de Apps Móviles"
Descripción: "Apps nativas iOS y Android..."
Ícono: "mobile-screen"
```

**3.3 Landing Legal:**

```
Slug: "legal"
Nombre: "SmartSolutions Legal"
Hero Título: "Digitaliza tu"
Hero Acento: "Bufete Legal"
...
```

**3.4 Landing Marketing:**

```
Slug: "marketing"
Nombre: "SmartSolutions Marketing"
Hero Título: "Crece tu Marca"
Hero Acento: "Online"
...
```

### Paso 4: Personalizar Colores por Landing (30 min)

**Opción A: CSS Variables Dinámicas**

```html
<!-- templates/landing/index.html -->
{% if config.color_primary %}
<style>
    :root {
        --brand-blue-600: {{ config.color_primary }};
        --brand-green-600: {{ config.color_secondary }};
    }
</style>
{% endif %}
```

**Opción B: Tailwind Config Dinámico**

```html
<script>
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    'brand-blue': {
                        600: '{{ config.color_primary|default:"#0066FF" }}',
                    },
                    'brand-green': {
                        600: '{{ config.color_secondary|default:"#10B981" }}',
                    },
                }
            }
        }
    }
</script>
```

### Paso 5: Admin Mejorado (1 hora)

**5.1 Admin Organizado:**

```python
# apps/core/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin

@admin.register(ConfiguracionLanding)
class ConfiguracionLandingAdmin(ModelAdmin):
    list_display = ['nombre', 'slug', 'activa', 'email_contacto']
    list_filter = ['activa']
    search_fields = ['nombre', 'slug']

    fieldsets = (
        ('Identificación', {
            'fields': ('nombre', 'slug', 'activa')
        }),
        ('Contacto', {
            'fields': ('email_contacto', 'whatsapp_numero')
        }),
        ('Hero Section', {
            'fields': (
                'hero_titulo_principal',
                'hero_titulo_acento',
                'hero_subtitulo',
            )
        }),
        ('Métricas', {
            'fields': (
                ('metrica_1_label', 'metrica_1_valor'),
                ('metrica_2_label', 'metrica_2_valor'),
                ('metrica_3_label', 'metrica_3_valor'),
            )
        }),
        ('SEO', {
            'fields': ('meta_titulo', 'meta_descripcion'),
            'classes': ('collapse',)
        }),
        ('Diseño', {
            'fields': ('color_primary', 'color_secondary'),
            'classes': ('collapse',)
        }),
        ('Redes Sociales', {
            'fields': ('linkedin_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
    )
```

**5.2 Filtro en Admin de Servicios:**

```python
@admin.register(Servicio)
class ServicioAdmin(ModelAdmin):
    list_display = ['titulo', 'landing', 'activo', 'orden']
    list_filter = ['activo', 'landing']  # ← Filtrar por landing
    search_fields = ['titulo', 'descripcion_corta']
```

### Paso 6: Testing (30 min)

```bash
# Verificar landings
http://localhost:8000/              # Landing principal
http://localhost:8000/tech/         # Landing tech
http://localhost:8000/legal/        # Landing legal
http://localhost:8000/marketing/    # Landing marketing
```

**Checklist:**

- [ ] Todas las URLs cargan correctamente
- [ ] Colores personalizados aplicados
- [ ] Servicios correctos por landing
- [ ] Testimonios correctos por landing
- [ ] Formulario envía a email correcto
- [ ] WhatsApp correcto por landing

### Resultado Final

✅ Sistema multi-landing operativo
✅ 4+ landing pages con contenido único
✅ Admin organizado por landing
✅ Colores personalizados por landing
✅ Fácil agregar nuevas landings

---

## ✅ Checklist de Lanzamiento

### Pre-Lanzamiento

**Contenido:**
- [ ] Todos los textos revisados (sin typos)
- [ ] Imágenes optimizadas (<500KB cada una)
- [ ] Logo en alta resolución
- [ ] Videos (si aplica) con subtítulos
- [ ] CTAs claros y accionables

**SEO:**
- [ ] Meta título único (<60 caracteres)
- [ ] Meta descripción atractiva (<160 caracteres)
- [ ] Alt text en todas las imágenes
- [ ] URLs amigables (slug descriptivo)
- [ ] Open Graph image (1200x630px)
- [ ] Sitemap.xml generado

**Funcionalidad:**
- [ ] Formulario de contacto funciona
- [ ] Emails de notificación llegan
- [ ] Auto-respuesta al cliente funciona
- [ ] WhatsApp button funciona
- [ ] Links internos correctos
- [ ] Links externos se abren en nueva pestaña

**Performance:**
- [ ] Lighthouse score >90
- [ ] Tiempo de carga <3 segundos
- [ ] Imágenes lazy loading
- [ ] CSS/JS minificados
- [ ] Cache configurado

**Mobile:**
- [ ] Responsive en todas las secciones
- [ ] Texto legible sin zoom
- [ ] Botones fáciles de clickear
- [ ] Menú móvil funciona
- [ ] Formulario usable en móvil

**Cross-Browser:**
- [ ] Chrome (última versión)
- [ ] Firefox (última versión)
- [ ] Safari (última versión)
- [ ] Edge (última versión)

### Post-Lanzamiento (Primera Semana)

**Analytics:**
- [ ] Google Analytics instalado
- [ ] Google Search Console conectado
- [ ] Eventos personalizados trackeados
- [ ] Conversiones configuradas

**Marketing:**
- [ ] Anuncio en redes sociales
- [ ] Email a base de datos existente
- [ ] Post en LinkedIn
- [ ] Story en Instagram

**Monitoreo:**
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Error tracking (Sentry)
- [ ] Revisar logs diariamente
- [ ] Verificar formularios funcionan

---

## 💡 Casos de Uso Comunes

### Caso 1: Landing para Evento

**Escenario:** Conferencia de tecnología en Valencia.

**Secciones necesarias:**
1. Hero con fecha y lugar
2. Speakers destacados
3. Agenda del evento
4. Patrocinadores
5. Formulario de registro

**Personalización:**

```html
<!-- _speakers.html -->
<section class="py-32">
    <h2>Speakers</h2>
    {% for speaker in speakers %}
        <div class="speaker-card">
            <img src="{{ speaker.foto }}" alt="{{ speaker.nombre }}">
            <h3>{{ speaker.nombre }}</h3>
            <p>{{ speaker.cargo }} - {{ speaker.empresa }}</p>
            <p>{{ speaker.bio }}</p>
        </div>
    {% endfor %}
</section>
```

**Modelo:**

```python
class Speaker(models.Model):
    nombre = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='speakers/')
    cargo = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    bio = models.TextField()
    orden = models.IntegerField()
```

**Formulario personalizado:**

```python
class RegistroEventoForm(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    empresa = forms.CharField()
    cargo = forms.CharField()
    tipo_entrada = forms.ChoiceField(choices=[
        ('general', 'General - $50'),
        ('vip', 'VIP - $150'),
        ('speaker', 'Speaker - Gratis'),
    ])
```

---

### Caso 2: Landing de Producto SaaS

**Escenario:** App de gestión de proyectos.

**Secciones:**
1. Hero con demo interactivo
2. Features principales
3. Pricing con 3 planes
4. Casos de uso
5. FAQ
6. Free trial signup

**Personalización:**

```html
<!-- _pricing.html -->
<section class="py-32 bg-neutral-50">
    <h2 class="text-center mb-16">Planes y Precios</h2>

    <div class="grid grid-cols-3 gap-8 max-w-6xl mx-auto">
        {% for plan in planes %}
        <div class="pricing-card {% if plan.destacado %}destacado{% endif %}">
            <h3>{{ plan.nombre }}</h3>
            <div class="precio">
                <span class="moneda">$</span>
                <span class="cantidad">{{ plan.precio }}</span>
                <span class="periodo">/mes</span>
            </div>

            <ul class="features">
                {% for feature in plan.features %}
                <li>
                    {% if feature.incluido %}✓{% else %}✗{% endif %}
                    {{ feature.nombre }}
                </li>
                {% endfor %}
            </ul>

            <a href="{{ plan.signup_url }}" class="btn-primary">
                {% if plan.free %}Comenzar Gratis{% else %}Suscribirse{% endif %}
            </a>
        </div>
        {% endfor %}
    </div>
</section>
```

---

### Caso 3: Landing Inmobiliaria

**Escenario:** Venta de apartamentos nuevos.

**Secciones:**
1. Hero con galería de fotos
2. Ubicación (mapa interactivo)
3. Planos disponibles
4. Amenidades
5. Calculadora de hipoteca
6. Tour virtual 360°

**Modelo:**

```python
class Apartamento(models.Model):
    nombre = models.CharField(max_length=100)  # "Modelo A"
    habitaciones = models.IntegerField()
    banos = models.DecimalField(max_digits=3, decimal_places=1)
    metros_cuadrados = models.DecimalField(max_digits=6, decimal_places=2)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    plano = models.ImageField(upload_to='planos/')
    disponibles = models.IntegerField()
```

**Widget calculadora:**

```html
<!-- _calculadora.html -->
<div x-data="{
    precio: 150000,
    inicial: 30000,
    anos: 20,
    tasa: 12.5,
    get cuota() {
        let monto = this.precio - this.inicial;
        let meses = this.anos * 12;
        let tasaMensual = this.tasa / 100 / 12;
        return (monto * tasaMensual * Math.pow(1 + tasaMensual, meses)) /
               (Math.pow(1 + tasaMensual, meses) - 1);
    }
}">
    <input type="range" x-model="precio" min="100000" max="500000" step="10000">
    <p>Precio: $<span x-text="precio.toLocaleString()"></span></p>

    <input type="range" x-model="inicial" min="0" :max="precio * 0.5" step="5000">
    <p>Inicial: $<span x-text="inicial.toLocaleString()"></span></p>

    <input type="range" x-model="anos" min="5" max="30">
    <p>Años: <span x-text="anos"></span></p>

    <div class="resultado">
        <h3>Cuota Mensual Estimada</h3>
        <p class="cuota">$<span x-text="cuota.toFixed(2)"></span></p>
    </div>
</div>
```

---

## 🎯 Tips Finales

### Do's ✅

1. **Mantén el contenido conciso** - Menos es más
2. **Usa imágenes de alta calidad** - Invierte en buenas fotos
3. **CTAs claros** - "Agenda tu consulta gratis" mejor que "Contactar"
4. **Social proof** - Testimonios, logos de clientes, métricas
5. **Mobile-first** - Diseña primero para móvil
6. **Carga rápida** - Optimiza todo
7. **A/B testing** - Prueba diferentes versiones
8. **Actualiza regularmente** - Contenido fresco = mejor SEO

### Don'ts ❌

1. **Mucho texto** - Nadie lee párrafos largos
2. **Imágenes pesadas** - >1MB es demasiado
3. **Muchos colores** - Máximo 3-4 colores
4. **Pop-ups agresivos** - No al popup inmediato
5. **Auto-play videos** - Molesto y consume datos
6. **Formularios largos** - Máximo 5 campos
7. **Links rotos** - Verificar regularmente
8. **Contenido desactualizado** - Revisar cada 3 meses

---

## 📞 Soporte

**¿Necesitas ayuda?**

- 📖 Leer `DOCUMENTATION.md`
- 🚀 Revisar `RECOMMENDATIONS.md`
- 💬 Contactar soporte: contacto@smartsolutions.ve
- 📱 WhatsApp: +58 412 169 1851

---

**¡Éxito creando tus landing pages!** 🎉

---

**Última actualización:** Febrero 2026
**Versión:** 1.0.0
