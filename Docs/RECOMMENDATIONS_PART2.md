# 🚀 Recomendaciones - Parte 2

## 📊 Analytics y Métricas

### 1. Google Analytics 4

**Implementación:**

```html
<!-- templates/base.html -->
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Eventos personalizados:**

```javascript
// Cuando usuario llena formulario
gtag('event', 'generate_lead', {
    'event_category': 'engagement',
    'event_label': 'contact_form',
    'value': 1
});

// Cuando descarga recurso
gtag('event', 'download', {
    'event_category': 'engagement',
    'event_label': 'whitepaper',
    'file_name': 'guia-transformacion-digital.pdf'
});

// Cuando hace clic en WhatsApp
gtag('event', 'contact_whatsapp', {
    'event_category': 'engagement',
    'event_label': 'whatsapp_button'
});
```

**Métricas clave a trackear:**

- Tasa de conversión (visitantes → leads)
- Tiempo en página
- Scroll depth (qué tan abajo llegan)
- Clics en CTAs
- Fuentes de tráfico
- Páginas de salida

---

### 2. Heatmaps con Hotjar

**¿Por qué?** Ver cómo los usuarios interactúan con tu landing.

```html
<!-- Hotjar Tracking Code -->
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:XXXXXXX,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
```

**Insights que obtendrás:**

- Heatmaps de clics
- Mapas de movimiento del mouse
- Grabaciones de sesiones
- Encuestas en página
- Funnels de conversión

---

### 3. Dashboard de Métricas Interno

```python
# apps/analytics/models.py
class Metrica(models.Model):
    """Almacenar métricas key del negocio"""
    fecha = models.DateField()

    # Tráfico
    visitantes_unicos = models.IntegerField(default=0)
    visitas_totales = models.IntegerField(default=0)
    paginas_vistas = models.IntegerField(default=0)

    # Conversión
    leads_generados = models.IntegerField(default=0)
    tasa_conversion = models.DecimalField(max_digits=5, decimal_places=2)

    # Engagement
    tiempo_promedio_pagina = models.IntegerField(help_text="En segundos")
    tasa_rebote = models.DecimalField(max_digits=5, decimal_places=2)

    # Fuentes
    trafico_organico = models.IntegerField(default=0)
    trafico_directo = models.IntegerField(default=0)
    trafico_referido = models.IntegerField(default=0)
    trafico_social = models.IntegerField(default=0)
    trafico_pago = models.IntegerField(default=0)

    class Meta:
        ordering = ['-fecha']
```

```python
# apps/analytics/views.py
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncMonth
import plotly.express as px

def dashboard_analitico(request):
    """Dashboard con visualizaciones"""

    # Métricas del mes actual
    mes_actual = Metrica.objects.filter(
        fecha__year=timezone.now().year,
        fecha__month=timezone.now().month
    ).aggregate(
        visitantes=Sum('visitantes_unicos'),
        leads=Sum('leads_generados'),
        conversion=Avg('tasa_conversion')
    )

    # Tendencia últimos 6 meses
    tendencia = Metrica.objects.filter(
        fecha__gte=timezone.now() - timedelta(days=180)
    ).annotate(
        mes=TruncMonth('fecha')
    ).values('mes').annotate(
        visitantes=Sum('visitantes_unicos'),
        leads=Sum('leads_generados')
    ).order_by('mes')

    # Gráfico con Plotly
    df = pd.DataFrame(list(tendencia))
    fig = px.line(df, x='mes', y=['visitantes', 'leads'], title='Tendencia Tráfico y Leads')
    grafico_html = fig.to_html()

    # Fuentes de tráfico (pie chart)
    fuentes = Metrica.objects.filter(
        fecha__gte=timezone.now() - timedelta(days=30)
    ).aggregate(
        organico=Sum('trafico_organico'),
        directo=Sum('trafico_directo'),
        referido=Sum('trafico_referido'),
        social=Sum('trafico_social'),
        pago=Sum('trafico_pago')
    )

    context = {
        'mes_actual': mes_actual,
        'grafico_tendencia': grafico_html,
        'fuentes': fuentes,
    }

    return render(request, 'analytics/dashboard.html', context)
```

**Command para sincronizar con Google Analytics:**

```python
# management/commands/sync_ga.py
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest

class Command(BaseCommand):
    help = 'Sincronizar métricas desde Google Analytics'

    def handle(self, *args, **kwargs):
        client = BetaAnalyticsDataClient()

        request = RunReportRequest(
            property=f"properties/{settings.GA_PROPERTY_ID}",
            date_ranges=[{"start_date": "7daysAgo", "end_date": "today"}],
            metrics=[
                {"name": "activeUsers"},
                {"name": "sessions"},
                {"name": "pageviews"},
            ],
        )

        response = client.run_report(request)

        # Guardar en DB
        for row in response.rows:
            Metrica.objects.create(
                fecha=row.dimension_values[0].value,
                visitantes_unicos=row.metric_values[0].value,
                # ... más campos
            )

        self.stdout.write(self.style.SUCCESS('Métricas sincronizadas'))
```

**Ejecutar diariamente con cron:**

```bash
# crontab -e
0 2 * * * cd /path/to/project && python manage.py sync_ga
```

---

## 🔒 Seguridad y Compliance

### 1. GDPR / Protección de Datos

**¿Por qué?** Ley de protección de datos (obligatorio en EU, buena práctica global).

```python
# apps/legal/models.py
class ConsentimientoGDPR(models.Model):
    """Registro de consentimientos"""
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)

    # Consentimientos
    acepta_terminos = models.BooleanField(default=False)
    acepta_marketing = models.BooleanField(default=False)
    acepta_cookies = models.BooleanField(default=False)

    # Auditoría
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    fecha_consentimiento = models.DateTimeField(auto_now_add=True)

class SolicitudBorrado(models.Model):
    """Derecho al olvido (GDPR)"""
    email = models.EmailField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)
    fecha_procesado = models.DateTimeField(null=True, blank=True)
```

**Banner de cookies:**

```html
<!-- templates/components/cookie_banner.html -->
<div id="cookie-banner" x-data="{ show: !localStorage.getItem('cookies_accepted') }" x-show="show"
     class="fixed bottom-0 left-0 right-0 bg-neutral-900 text-white p-6 shadow-2xl z-50">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-6 flex-wrap">
        <p class="text-sm">
            Usamos cookies para mejorar tu experiencia. Al continuar navegando, aceptas nuestra
            <a href="/politica-privacidad" class="underline">Política de Privacidad</a>.
        </p>
        <div class="flex gap-4">
            <button @click="localStorage.setItem('cookies_accepted', 'true'); show = false"
                    class="px-6 py-2 bg-brand-blue-600 rounded-lg font-bold hover:bg-brand-blue-700">
                Aceptar
            </button>
            <button @click="show = false"
                    class="px-6 py-2 bg-neutral-700 rounded-lg font-bold hover:bg-neutral-600">
                Rechazar
            </button>
        </div>
    </div>
</div>
```

**Páginas legales necesarias:**

```
/politica-privacidad       - Cómo se usan los datos
/terminos-condiciones      - Términos de uso del sitio
/politica-cookies          - Qué cookies se usan
/borrar-mis-datos          - Formulario GDPR
```

---

### 2. Rate Limiting

**¿Por qué?** Prevenir spam y ataques DoS.

```bash
pip install django-ratelimit
```

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/h', method='POST')  # 5 envíos por hora por IP
def contacto_submit(request):
    """Formulario protegido contra spam"""

    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return HttpResponse(
            'Demasiados intentos. Intenta de nuevo en 1 hora.',
            status=429
        )

    # ... resto del código
```

**Rate limits sugeridos:**

```python
# Formulario contacto: 5 por hora
@ratelimit(key='ip', rate='5/h', method='POST')

# API pública: 100 por hora
@ratelimit(key='ip', rate='100/h')

# Login: 5 intentos por 15 minutos
@ratelimit(key='ip', rate='5/15m', method='POST')
```

---

### 3. Web Application Firewall (WAF)

**Opciones:**

#### A. Cloudflare WAF (Gratis/Paid)

1. Agregar sitio a Cloudflare
2. Activar WAF en Security → WAF
3. Reglas automáticas contra:
   - SQL Injection
   - XSS
   - CSRF
   - DDoS

#### B. ModSecurity (Open Source)

```bash
# En servidor con Nginx
sudo apt-get install libnginx-mod-security
```

Reglas OWASP Core Rule Set incluidas.

---

### 4. Backup Automático

```python
# management/commands/backup_db.py
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Backup de base de datos PostgreSQL'

    def handle(self, *args, **kwargs):
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_{timestamp}.sql'

        # Backup PostgreSQL
        subprocess.run([
            'pg_dump',
            '-U', settings.DATABASES['default']['USER'],
            '-h', settings.DATABASES['default']['HOST'],
            settings.DATABASES['default']['NAME'],
            '-f', backup_file
        ])

        # Subir a S3
        import boto3
        s3 = boto3.client('s3')
        s3.upload_file(
            backup_file,
            'smartsolutions-backups',
            f'db/{backup_file}'
        )

        # Limpiar backups antiguos (>30 días)
        # ...

        self.stdout.write(self.style.SUCCESS(f'Backup creado: {backup_file}'))
```

**Ejecutar diariamente:**

```bash
# crontab -e
0 3 * * * cd /path/to/project && python manage.py backup_db
```

---

### 5. Monitoreo de Seguridad

**A. Sentry (Error Tracking + Security)**

```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://xxx@sentry.io/xxx",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment='production'
)
```

**B. Security Headers**

```python
# settings.py (producción)
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

**Verificar con:** https://securityheaders.com/

---

## ⚡ Performance y Optimización

### 1. Database Optimization

**Índices estratégicos:**

```python
class Lead(models.Model):
    # ... campos

    class Meta:
        indexes = [
            models.Index(fields=['email']),  # Búsquedas frecuentes
            models.Index(fields=['estado', 'fecha_creacion']),  # Filtros comunes
            models.Index(fields=['-fecha_creacion']),  # Ordenamiento
        ]
```

**Query optimization:**

```python
# ❌ Malo: N+1 queries
for servicio in Servicio.objects.all():
    print(servicio.categoria.nombre)  # Query por cada servicio

# ✅ Bueno: 1 query
servicios = Servicio.objects.select_related('categoria').all()
for servicio in servicios:
    print(servicio.categoria.nombre)
```

```python
# ❌ Malo: Cargar objetos completos
leads = Lead.objects.all()  # Carga TODOS los campos

# ✅ Bueno: Solo campos necesarios
leads = Lead.objects.values('nombre', 'email', 'estado')
```

**Database connection pooling:**

```bash
pip install psycopg2-binary pgbouncer
```

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=10000'  # 10 segundos
        },
        'CONN_MAX_AGE': 600,  # Mantener conexiones 10 minutos
    }
}
```

---

### 2. Lazy Loading de Imágenes

```html
<!-- Native lazy loading -->
<img src="imagen.jpg"
     loading="lazy"
     alt="Descripción">

<!-- Con IntersectionObserver (más control) -->
<img data-src="imagen.jpg"
     class="lazy"
     alt="Descripción">

<script>
document.addEventListener("DOMContentLoaded", function() {
    const lazyImages = document.querySelectorAll('.lazy');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    lazyImages.forEach(img => imageObserver.observe(img));
});
</script>
```

---

### 3. Image Optimization

```bash
# Instalar Pillow con optimizadores
pip install Pillow pillow-avif-plugin

# Instalar herramientas de optimización
sudo apt-get install jpegoptim optipng pngquant
```

```python
# apps/core/utils.py
from PIL import Image
import io

def optimizar_imagen(imagen_file):
    """Optimizar imagen automáticamente"""
    img = Image.open(imagen_file)

    # Convertir a RGB si es necesario
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Redimensionar si es muy grande
    max_size = (1920, 1080)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)

    # Guardar optimizado
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=85, optimize=True)
    output.seek(0)

    return output
```

**Usar en modelos:**

```python
class Caso(models.Model):
    imagen = models.ImageField(upload_to='casos/')

    def save(self, *args, **kwargs):
        if self.imagen:
            self.imagen = optimizar_imagen(self.imagen)
        super().save(*args, **kwargs)
```

**Servir en formato moderno (WebP/AVIF):**

```html
<picture>
    <source srcset="imagen.avif" type="image/avif">
    <source srcset="imagen.webp" type="image/webp">
    <img src="imagen.jpg" alt="Fallback">
</picture>
```

---

### 4. Minificar CSS/JS en Producción

```bash
pip install django-compressor
```

```python
# settings.py
INSTALLED_APPS += ['compressor']

STATICFILES_FINDERS += ['compressor.finders.CompressorFinder']

COMPRESS_ENABLED = True  # Solo en producción
COMPRESS_OFFLINE = True  # Pre-comprimir en deploy
```

```html
{% load compress %}

{% compress css %}
    <link rel="stylesheet" href="{% static 'css/design-system.css' %}">
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
{% endcompress %}

{% compress js %}
    <script src="{% static 'js/main.js' %}"></script>
{% endcompress %}
```

---

### 5. Monitoring con New Relic

```bash
pip install newrelic
```

```bash
# Generar config
newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini
```

```bash
# Ejecutar con New Relic
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn smartsolutions.wsgi
```

**Métricas que trackea:**

- Response time por endpoint
- Queries lentas de DB
- External services (APIs)
- Error rate
- Throughput (requests/min)
- Apdex score

---

## 💰 Monetización y Productización

### 1. Modelo SaaS (Software as a Service)

**¿Para qué?** Ofrecer tu sistema de landing pages a otras empresas.

```python
# apps/saas/models.py
class Plan(models.Model):
    TIPO_CHOICES = [
        ('free', 'Gratis'),
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]

    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    precio_anual = models.DecimalField(max_digits=10, decimal_places=2)

    # Límites
    max_landing_pages = models.IntegerField()
    max_leads_mes = models.IntegerField()
    max_usuarios = models.IntegerField()
    max_storage_mb = models.IntegerField()

    # Features
    analytics_avanzado = models.BooleanField(default=False)
    api_access = models.BooleanField(default=False)
    white_label = models.BooleanField(default=False)
    soporte_prioritario = models.BooleanField(default=False)

class Suscripcion(models.Model):
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)

    # Fechas
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    # Billing
    stripe_customer_id = models.CharField(max_length=200, blank=True)
    stripe_subscription_id = models.CharField(max_length=200, blank=True)
```

**Precios sugeridos:**

```
┌──────────────┬──────────┬──────────────┬────────────┬──────────────┐
│     Plan     │  Precio  │   Landings   │ Leads/mes  │   Features   │
├──────────────┼──────────┼──────────────┼────────────┼──────────────┤
│ Free         │   $0     │      1       │    100     │   Básico     │
│ Starter      │  $29/mes │      3       │   1,000    │ + Analytics  │
│ Professional │  $99/mes │     10       │   5,000    │ + API        │
│ Enterprise   │ $299/mes │  Ilimitado   │  50,000    │ + White Label│
└──────────────┴──────────┴──────────────┴────────────┴──────────────┘
```

---

### 2. Integración con Stripe

```bash
pip install stripe
```

```python
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def crear_suscripcion(empresa, plan):
    """Crear suscripción en Stripe"""

    # Crear o recuperar customer
    if not empresa.stripe_customer_id:
        customer = stripe.Customer.create(
            email=empresa.email_contacto,
            name=empresa.nombre,
            metadata={'empresa_id': empresa.id}
        )
        empresa.stripe_customer_id = customer.id
        empresa.save()

    # Crear suscripción
    subscription = stripe.Subscription.create(
        customer=empresa.stripe_customer_id,
        items=[{'price': plan.stripe_price_id}],
        payment_behavior='default_incomplete',
        expand=['latest_invoice.payment_intent'],
    )

    # Guardar en DB
    Suscripcion.objects.create(
        empresa=empresa,
        plan=plan,
        stripe_subscription_id=subscription.id
    )

    return subscription
```

**Webhook para eventos de Stripe:**

```python
from django.views.decorators.csrf import csrf_exempt
import stripe

@csrf_exempt
def stripe_webhook(request):
    """Recibir eventos de Stripe"""
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Manejar eventos
    if event['type'] == 'invoice.paid':
        # Suscripción pagada exitosamente
        subscription_id = event['data']['object']['subscription']
        suscripcion = Suscripcion.objects.get(stripe_subscription_id=subscription_id)
        suscripcion.activa = True
        suscripcion.save()

    elif event['type'] == 'invoice.payment_failed':
        # Pago falló
        subscription_id = event['data']['object']['subscription']
        suscripcion = Suscripcion.objects.get(stripe_subscription_id=subscription_id)
        # Enviar email de recordatorio
        enviar_email_pago_fallido(suscripcion)

    elif event['type'] == 'customer.subscription.deleted':
        # Suscripción cancelada
        subscription_id = event['data']['object']['id']
        suscripcion = Suscripcion.objects.get(stripe_subscription_id=subscription_id)
        suscripcion.activa = False
        suscripcion.fecha_fin = timezone.now()
        suscripcion.save()

    return HttpResponse(status=200)
```

---

### 3. Marketplace de Templates

**¿Para qué?** Vender templates pre-diseñados de landing pages.

```python
# apps/marketplace/models.py
class TemplateLanding(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    preview_url = models.URLField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    # Archivos
    archivo_zip = models.FileField(upload_to='templates/')
    imagenes_preview = models.JSONField()  # Lista de URLs

    # Categoría
    categoria = models.CharField(max_length=100)
    tags = models.JSONField()  # ['tech', 'saas', 'minimal']

    # Ventas
    veces_vendido = models.IntegerField(default=0)
    rating_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    # Autor
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    comision_autor = models.DecimalField(max_digits=5, decimal_places=2)  # %

class CompraTemplate(models.Model):
    template = models.ForeignKey(TemplateLanding, on_delete=models.CASCADE)
    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    # Download
    download_token = models.UUIDField(default=uuid.uuid4, unique=True)
    veces_descargado = models.IntegerField(default=0)
```

**Precios sugeridos:**

```
Template Simple: $29
Template Professional: $79
Template Enterprise: $149
Bundle (5 templates): $299
```

---

### 4. Servicios Complementarios

**A. Done-For-You (DFY):**

```
Setup Completo: $499
├── Instalación y configuración
├── Diseño personalizado
├── Carga de contenido
├── SEO básico
└── Training 2 horas
```

**B. Mantenimiento Mensual:**

```
Plan Mantenimiento: $99/mes
├── Updates de software
├── Backups diarios
├── Monitoreo 24/7
├── Soporte prioritario
└── 2 horas de cambios/mes
```

**C. Consultoría:**

```
Consultoría Estratégica: $150/hora
├── Optimización de conversión
├── Estrategia de contenido
├── Automatización de marketing
└── Análisis de métricas
```

---

## 🤖 Automatización y DevOps

### 1. CI/CD con GitHub Actions

```yaml
# .github/workflows/django.yml
name: Django CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest --cov

    - name: Lint with flake8
      run: |
        flake8 apps/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - name: Deploy to production
      run: |
        # Deploy to Heroku, Railway, etc.
        git push heroku main
```

---

### 2. Docker para Desarrollo

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dependencias sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Recolectar estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "smartsolutions.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: smartsolutions
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    env_file:
      - .env

volumes:
  postgres_data:
```

**Ejecutar:**

```bash
docker-compose up
```

---

### 3. Automatización de Tasks

```bash
# Instalar Celery para tareas async
pip install celery redis
```

```python
# smartsolutions/celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartsolutions.settings')

app = Celery('smartsolutions')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

```python
# apps/landing/tasks.py
from celery import shared_task

@shared_task
def enviar_email_async(lead_id):
    """Enviar email de forma asíncrona"""
    lead = Lead.objects.get(id=lead_id)
    enviar_email_notificacion(lead)

@shared_task
def generar_reporte_mensual():
    """Generar reporte automático"""
    # ... lógica
    pass

@shared_task
def limpiar_leads_antiguos():
    """Limpiar leads >1 año sin actividad"""
    Lead.objects.filter(
        fecha_creacion__lt=timezone.now() - timedelta(days=365),
        estado='nuevo'
    ).delete()
```

**Ejecutar worker:**

```bash
celery -A smartsolutions worker -l info
```

**Tareas programadas (Celery Beat):**

```python
# settings.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'reporte-mensual': {
        'task': 'apps.landing.tasks.generar_reporte_mensual',
        'schedule': crontab(day_of_month=1, hour=8),  # 1ro de cada mes, 8am
    },
    'limpiar-leads': {
        'task': 'apps.landing.tasks.limpiar_leads_antiguos',
        'schedule': crontab(day_of_week=0, hour=2),  # Domingos, 2am
    },
}
```

**Ejecutar beat:**

```bash
celery -A smartsolutions beat -l info
```

---

## 🗺️ Roadmap Sugerido

### Q1 2026 (Meses 1-3): Fundación

**Mes 1: Estabilización**
- [x] Landing page principal completada
- [ ] Tests unitarios (80% coverage)
- [ ] CI/CD configurado
- [ ] Documentación completa
- [ ] SEO básico implementado

**Mes 2: Analytics y Mejora**
- [ ] Google Analytics 4 + Hotjar
- [ ] A/B testing en CTAs
- [ ] Optimización de conversión
- [ ] Email marketing setup (Mailchimp)
- [ ] Primeros 50 leads

**Mes 3: Automatización**
- [ ] CRM simple integrado
- [ ] Pipeline de ventas definido
- [ ] Auto-respuestas configuradas
- [ ] Dashboard de métricas
- [ ] Primeras 5 ventas

---

### Q2 2026 (Meses 4-6): Escalamiento

**Mes 4: Multi-Landing**
- [ ] Sistema de templates
- [ ] 3 landings adicionales creadas
- [ ] Sistema de referidos
- [ ] Portal de clientes básico

**Mes 5: Integraciones**
- [ ] Stripe payments
- [ ] API REST completa
- [ ] Webhook system
- [ ] Zapier integration

**Mes 6: Profesionalización**
- [ ] Internacionalización (ES, EN, PT)
- [ ] Chat en vivo (Tidio)
- [ ] Sistema de cotizaciones
- [ ] 100+ leads/mes

---

### Q3 2026 (Meses 7-9): Productización

**Mes 7: SaaS MVP**
- [ ] Multi-tenancy implementado
- [ ] 3 planes de precios definidos
- [ ] Self-service signup
- [ ] Primeros 10 clientes SaaS

**Mes 8: Marketplace**
- [ ] Marketplace de templates
- [ ] 5 templates en venta
- [ ] Sistema de comisiones
- [ ] Reviews y ratings

**Mes 9: Automatización Avanzada**
- [ ] Celery + Redis
- [ ] Email sequences automatizadas
- [ ] Reportes automáticos
- [ ] 50 clientes SaaS

---

### Q4 2026 (Meses 10-12): Expansión

**Mes 10: Mobile**
- [ ] App móvil (React Native/Flutter)
- [ ] Notificaciones push
- [ ] Lead management mobile

**Mes 11: White Label**
- [ ] Sistema white label completo
- [ ] Custom domains
- [ ] Branding personalizado
- [ ] 100 clientes SaaS

**Mes 12: Enterprise**
- [ ] Features enterprise
- [ ] SSO (Single Sign-On)
- [ ] Advanced analytics
- [ ] API rate limits customizables
- [ ] $10K+ MRR

---

## 📈 Métricas de Éxito

### Métricas de Producto

```
Usuarios/Clientes:
├── MAU (Monthly Active Users)
├── Tasa de retención (30, 60, 90 días)
├── Churn rate
└── NPS (Net Promoter Score)

Engagement:
├── Tiempo en plataforma
├── Landings creadas por usuario
├── Leads generados por landing
└── Tasa de conversión promedio

Financieras:
├── MRR (Monthly Recurring Revenue)
├── ARR (Annual Recurring Revenue)
├── ARPU (Average Revenue Per User)
├── LTV (Lifetime Value)
├── CAC (Customer Acquisition Cost)
└── LTV/CAC ratio (objetivo: >3)
```

### KPIs por Etapa

**Startup (0-100 clientes):**
- 20% MoM growth
- Churn < 10%
- NPS > 40

**Growth (100-1000 clientes):**
- 15% MoM growth
- Churn < 5%
- NPS > 50
- LTV/CAC > 3

**Scale (1000+ clientes):**
- 10% MoM growth
- Churn < 3%
- NPS > 60
- LTV/CAC > 5

---

## 🎯 Conclusión

Este proyecto tiene potencial de convertirse en:

1. **SaaS Rentable** - $10K-50K MRR en 12-18 meses
2. **Agencia Digital** - Servicios complementarios
3. **Marketplace** - Templates y plugins
4. **Enterprise Solution** - White label para grandes empresas

**Próximos pasos inmediatos:**

1. ✅ Completar testing y CI/CD
2. ✅ Optimizar SEO y analytics
3. ✅ Crear 2-3 templates adicionales
4. ✅ Implementar sistema de pagos
5. ✅ Lanzar MVP SaaS

**¡Éxito en tu journey de construir un producto exitoso!** 🚀

---

**Última actualización:** Febrero 2026
**Versión:** 1.0.0
