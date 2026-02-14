# PROMPT PARA CLAUDE CODE: SmartSolutions VE Landing Page

## CONTEXTO DEL PROYECTO

Estoy desarrollando la landing page oficial de **SmartSolutions VE**, mi empresa de consultoría tecnológica enfocada en PYMEs venezolanas. El objetivo es crear un sitio web profesional de captación de leads con panel admin integrado, que sirva como puerta de entrada a futuros productos SaaS.

---

## ARQUITECTURA Y STACK TECNOLÓGICO DEFINIDO

### Stack completo
- **Backend**: Django 5.0.4 + Django REST Framework
- **Frontend**: Django Templates + HTMX + Alpine.js (NO React/Vue)
- **Base de datos**: PostgreSQL (producción)
- **CMS**: Django Admin personalizado con django-unfold
- **Email**: Resend API (formulario de contacto)
- **Infraestructura**: VPS Hetzner CAX11 (~$4/mes) con Docker Compose
- **CI/CD**: GitHub Actions para deploy automático

### Razones de las decisiones técnicas
1. **Django desde el día uno**: El mismo servidor alojará el SaaS futuro, sin deuda técnica
2. **HTMX + Alpine.js**: Interactividad moderna sin complejidad de SPA
3. **Django Admin + Unfold**: CMS visual profesional sin necesidad de headless CMS externo
4. **Presupuesto**: <$10/mes (cumplido con Hetzner + Resend free tier)

---

## ESTADO ACTUAL DEL DESARROLLO

### ✅ FASE 1 COMPLETADA: Estructura del proyecto Django + CMS

**Lo que YA ESTÁ CONSTRUIDO:**

#### 1. Configuración base (`config/`)
- `settings.py`: Configuración completa con seguridad en producción, Django Unfold personalizado con colores SmartSolutions (#0066FF azul, #22C55E verde), variables de entorno via `python-decouple`
- `urls.py`, `wsgi.py`: configuración estándar
- `.env.example`: plantilla de variables de entorno

#### 2. App `core` - Configuración global
**Modelo**: `ConfiguracionSitio` (singleton)
- Identidad: nombre_empresa, slogan, descripcion_corta
- Contacto: email, WhatsApp (número + mensaje pre-cargado)
- Redes sociales: LinkedIn, Instagram, Twitter, Facebook
- SEO: meta_titulo, meta_descripcion
- Hero section: titulo_principal, titulo_acento, subtitulo
- Métricas del hero: 3 métricas con valor + label (ej: "+50 PYMEs transformadas")

**Context processor**: `site_config()` inyecta `{{ config }}` en todos los templates

**Admin**: Personalizado con django-unfold, organizado en fieldsets semánticos

#### 3. App `landing` - Contenido editable
**Modelos**:
- `Servicio`: titulo, descripcion_corta, descripcion_larga, icono (8 opciones), beneficio_clave, orden, activo
- `Testimonio`: nombre_cliente, cargo, empresa, sector, foto, texto, resultado_clave, orden, activo, destacado
- `CasoDeExito`: titulo, empresa, sector, descripcion, 3 métricas (valor + label), imagen, orden, activo
- `Lead`: nombre, email, telefono, empresa, servicio_interes, mensaje, estado (5 opciones), notas_internas, metadata (created_at, IP)

**Forms**: `ContactoForm` con validación y placeholders configurados

**Views**: 
- `landing()`: renderiza la página principal con todos los contenidos
- `contacto_submit()`: procesa formulario, guarda Lead, envía email via Resend con HTML profesional, soporta HTMX

**Admin**: Completo con django-unfold, list_display, list_filter, badges de color para estados de Leads

#### 4. Estructura de archivos
```
smartsolutions/
├── apps/
│   ├── core/           # Configuración global
│   └── landing/        # Contenido de la landing
├── config/             # Settings Django
├── static/             # CSS, JS, imágenes (VACÍO por ahora)
├── templates/          # Templates Django (VACÍO por ahora)
├── media/              # Uploads
├── .github/workflows/  # CI/CD (por configurar)
├── requirements.txt
├── manage.py
├── .env.example
└── .gitignore
```

---

## 🎯 FASE 2: TEMPLATES Y SISTEMA DE DISEÑO (LO QUE FALTA)

### OBJETIVO DE ESTA FASE
Crear el template base de Django con el sistema de diseño completo (variables CSS, tipografía, paleta de colores) y comenzar a construir las secciones de la landing page.

### LO QUE NECESITAS CREAR:

#### 1. Sistema de diseño en CSS (`static/css/base.css`)
**Variables CSS**:
```css
:root {
  /* Colores SmartSolutions VE */
  --color-primary: #0066FF;      /* Azul principal */
  --color-secondary: #22C55E;    /* Verde acento */
  --color-dark: #0A0A0A;         /* Negro casi puro */
  --color-gray-900: #1A1A1A;
  --color-gray-800: #2D2D2D;
  --color-gray-700: #404040;
  --color-gray-600: #666666;
  --color-gray-500: #808080;
  --color-gray-400: #999999;
  --color-gray-300: #CCCCCC;
  --color-gray-200: #E5E5E5;
  --color-gray-100: #F5F5F5;
  --color-white: #FFFFFF;

  /* Tipografía - Outfit (Google Fonts) */
  --font-primary: 'Outfit', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Espaciado */
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 1.5rem;
  --spacing-lg: 2rem;
  --spacing-xl: 3rem;
  --spacing-2xl: 4rem;
  --spacing-3xl: 6rem;

  /* Bordes */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-full: 9999px;

  /* Sombras */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  --shadow-primary: 0 10px 40px -5px rgba(0, 102, 255, 0.4);
  --shadow-secondary: 0 10px 40px -5px rgba(34, 197, 94, 0.3);

  /* Transiciones */
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
  --transition-slow: 350ms ease;
}
```

**IMPORTANTE**: Según el skill de frontend-design, EVITAR fuentes genéricas (Inter, Roboto, Arial). Usa **Outfit** como display font y **JetBrains Mono** para código/métricas.

#### 2. Template base (`templates/base.html`)
- HTML5 semántico
- Meta tags SEO dinámicos desde `{{ config }}`
- Open Graph para compartir en redes
- Google Fonts (Outfit + JetBrains Mono)
- HTMX CDN
- Alpine.js CDN
- Estructura:
  ```django
  <!DOCTYPE html>
  <html lang="es">
  <head>
    <!-- Meta, SEO, fonts -->
  </head>
  <body>
    {% include 'components/navbar.html' %}
    
    <main>
      {% block content %}{% endblock %}
    </main>
    
    {% include 'components/footer.html' %}
    
    <!-- Scripts -->
  </body>
  </html>
  ```

#### 3. Componentes base
- `templates/components/navbar.html`: Header fijo con logo, menú, botón WhatsApp
- `templates/components/footer.html`: Footer con redes sociales, copyright, links legales
- `templates/components/whatsapp_button.html`: Botón flotante de WhatsApp (sticky bottom-right)

#### 4. Secciones de la landing (`templates/landing/index.html`)
**ESTRUCTURA DEFINIDA** (según análisis previo del chat de SmartSolutions):

1. **Hero Section**
   - Headline orientado a resultado (desde `{{ config.hero_titulo_principal }}`)
   - Subtítulo que explica el problema (desde `{{ config.hero_subtitulo }}`)
   - CTA principal: "Obtener Diagnóstico Gratuito"
   - 3 métricas visuales (desde `{{ config.metrica_X_valor }}`)

2. **Problema + Solución**
   - "¿Te suena familiar?" + situaciones específicas
   - Consecuencias de no actuar
   - Tu metodología como única solución

3. **Servicios** (loop de `{% for servicio in servicios %}`)
   - Grid de cards con iconos
   - Título + descripción corta
   - Beneficio clave destacado

4. **Casos de Éxito** (loop de `{% for caso in casos %}`)
   - Cards con métricas cuantificables
   - Empresa + sector + descripción

5. **Testimonios** (loop de `{% for testimonio in testimonios %}`)
   - Slider/carousel
   - Foto + nombre + cargo + empresa
   - Testimonio + resultado clave

6. **Formulario de Contacto**
   - Integración con HTMX para envío sin recargar
   - Validación en tiempo real
   - Feedback visual (success/error)

---

## IDENTIDAD VISUAL Y DISEÑO

### Paleta de colores (ESTRICTA)
- **Primario**: Azul #0066FF (confianza, tecnología)
- **Secundario**: Verde #22C55E (crecimiento, éxito)
- **Base**: Escala de grises desde #0A0A0A hasta #F5F5F5
- **Fondo principal**: Gris oscuro #1A1A1A (tema oscuro profesional)
- **Texto principal**: Blanco #FFFFFF / Gris claro #F5F5F5

### Tipografía
- **Display / Headings**: Outfit (Google Fonts) - Bold 700, SemiBold 600
- **Body**: Outfit Regular 400
- **Métricas / Código**: JetBrains Mono

### Estética objetivo (basado en frontend-design skill)
- **Tono**: Profesional pero moderno, confiable pero innovador
- **NO USAR**: Purple gradients, glassmorphism genérico, Inter/Roboto/Arial
- **SÍ USAR**: Asymmetry, overlap, generous negative space, bold color accents, subtle animations on scroll
- **Inspiración**: Dashboards B2B modernos, pero con personalidad latinoamericana (no tan fríos)

---

## FUNCIONALIDADES TÉCNICAS CLAVE

### HTMX en el formulario
```html
<form 
  hx-post="{% url 'landing:contacto_submit' %}" 
  hx-target="#form-container"
  hx-swap="outerHTML"
>
  <!-- campos del formulario -->
</form>
```

Al enviar:
- Si OK → renderiza `templates/components/contacto_success.html`
- Si error → re-renderiza el form con errores visibles

### Alpine.js para micro-interacciones
```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open">Contenido</div>
</div>
```

Úsalo para: menú móvil, acordeones, counters animados de las métricas

---

## ALCANCE DEL PRODUCTO FINAL

### Visión completa
Una landing page de conversión profesional que:
1. Captura leads calificados de PYMEs venezolanas interesadas en transformación digital
2. Se edita 100% desde el admin de Django (textos, servicios, testimonios, casos)
3. Envía notificaciones email automáticas al recibir contactos
4. Es responsive, rápida (<2s carga), y optimizada para SEO
5. Sirve como base de infraestructura para el futuro SaaS (mismo servidor, misma DB)

### Métricas de éxito
- Tasa de conversión objetivo: 3-5% (visitantes → formulario enviado)
- Tiempo de carga: <2 segundos
- Puntuación Lighthouse: >90 en todas las categorías
- 100% editable sin tocar código (requisito del cliente/dueño)

### Roadmap post-lanzamiento
1. **Fase 3**: Docker Compose + deployment en Hetzner
2. **Fase 4**: CI/CD con GitHub Actions
3. **Fase 5**: Optimizaciones SEO avanzadas + Analytics
4. **Futuro**: El SaaS se añadirá bajo `/app` en el mismo dominio

---

## INSTRUCCIONES PARA CLAUDE CODE

### Tu rol
Eres el desarrollador frontend senior que toma la estructura Django ya construida y la convierte en una landing page visualmente impactante, profesional y funcional.

### Prioridades
1. **Diseño distintivo**: Evita clichés de IA (purple gradients, Inter fonts). Usa la paleta SmartSolutions con personalidad.
2. **Performance**: CSS puro siempre que sea posible. JS mínimo. HTMX para AJAX.
3. **Responsive**: Mobile-first approach obligatorio (80% del tráfico será móvil desde Venezuela)
4. **SEO**: Estructura semántica, meta tags dinámicos, schema.org markup
5. **Accesibilidad**: ARIA labels, contrast ratios, keyboard navigation

### Flujo de trabajo sugerido
1. Crea `static/css/base.css` con el sistema de diseño completo
2. Construye `templates/base.html` con la estructura base
3. Implementa los componentes: navbar, footer, whatsapp_button
4. Desarrolla cada sección de `landing/index.html` una por una
5. Añade interactividad con HTMX + Alpine.js
6. Optimiza y refina

### Restricciones técnicas
- **NO** uses librerías CSS externas (Bootstrap, Tailwind). CSS puro con variables CSS.
- **NO** uses jQuery. Solo HTMX + Alpine.js.
- **SÍ** usa animaciones CSS nativas (`@keyframes`, `transition`, `animation`)
- **SÍ** implementa lazy loading de imágenes
- **SÍ** optimiza para Core Web Vitals

---

## PREGUNTAS PARA EMPEZAR

Antes de comenzar, confirma:
1. ¿Entiendes la arquitectura y el estado actual del proyecto?
2. ¿Está clara la estética visual que buscamos (profesional + moderna + NO genérica)?
3. ¿Necesitas aclaraciones sobre algún modelo o funcionalidad del backend?
4. ¿Prefieres que abordemos sección por sección o prefieres un entregable completo al final?

Una vez confirmado, comienza con el sistema de diseño en `static/css/base.css` y el template `base.html`.

---

## CONTEXTO ADICIONAL DEL NEGOCIO

**SmartSolutions VE** ofrece:
- Automatización de procesos para PYMEs
- Dashboards de inteligencia de negocios
- Software a medida (ERP, CRM, inventarios)
- Consultoría en transformación digital
- Integración con sistemas legacy (muy común en Venezuela: Saint ERP, Profit Plus, Admin PAQ)

**Público objetivo**:
- Dueños de PYMEs venezolanas (10-100 empleados)
- Sectores: distribuidoras, farmacias, ferreterías, talleres, construcción
- Edad: 35-55 años
- Pain points: procesos manuales, datos en Excel, decisiones por intuición, pérdida de control operativo

**Propuesta de valor diferencial**:
- Conocimiento profundo del mercado venezolano (doble moneda, IVA, contexto económico)
- ROI medible en 90 días o menos
- Acompañamiento continuo post-implementación
- Precios accesibles adaptados a la realidad local

**Tono de comunicación**:
- Profesional pero cercano
- Directo, sin tecnicismos innecesarios
- Enfocado en resultados tangibles (%, $, tiempo)
- Empatía con las dificultades del empresario venezolano

---

¡Manos a la obra! Comienza con el sistema de diseño y el template base. Avanza paso a paso, mostrándome cada pieza antes de continuar a la siguiente.
