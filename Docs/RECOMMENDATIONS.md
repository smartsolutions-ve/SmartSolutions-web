# 🚀 Recomendaciones para Profesionalizar SmartSolutions

> Guía completa de mejoras técnicas, de negocio y estratégicas para llevar tu producto al siguiente nivel.

---

## 📑 Tabla de Contenidos

1. [Mejoras Técnicas Inmediatas](#mejoras-técnicas-inmediatas)
2. [Mejoras de Negocio](#mejoras-de-negocio)
3. [Escalabilidad y Arquitectura](#escalabilidad-y-arquitectura)
4. [SEO y Marketing Digital](#seo-y-marketing-digital)
5. [Analytics y Métricas](#analytics-y-métricas)
6. [Seguridad y Compliance](#seguridad-y-compliance)
7. [Performance y Optimización](#performance-y-optimización)
8. [Monetización y Productización](#monetización-y-productización)
9. [Automatización y DevOps](#automatización-y-devops)
10. [Roadmap Sugerido](#roadmap-sugerido)

---

## 🔧 Mejoras Técnicas Inmediatas

### 1. Sistema de Testing

**¿Por qué?** Garantiza que los cambios no rompan funcionalidad existente.

**Implementación:**

```bash
# Instalar pytest
pip install pytest pytest-django pytest-cov
```

```python
# tests/test_models.py
import pytest
from apps.core.models import ConfiguracionSitio
from apps.landing.models import Lead

@pytest.mark.django_db
def test_configuracion_singleton():
    """Solo debe existir una configuración"""
    config1 = ConfiguracionSitio.objects.create(nombre_empresa="Test")
    config2 = ConfiguracionSitio.objects.create(nombre_empresa="Test2")

    assert ConfiguracionSitio.objects.count() == 1

@pytest.mark.django_db
def test_lead_creation():
    """Verificar creación de leads"""
    lead = Lead.objects.create(
        nombre="Juan Test",
        email="juan@test.com",
        mensaje="Mensaje de prueba"
    )
    assert lead.estado == 'nuevo'
    assert str(lead) == "Juan Test - juan@test.com"
```

```python
# tests/test_views.py
def test_index_view(client):
    """Verificar que la página principal carga"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'SmartSolutions' in str(response.content)

def test_contacto_submit(client):
    """Verificar envío de formulario"""
    data = {
        'nombre': 'Test User',
        'email': 'test@example.com',
        'mensaje': 'Test message'
    }
    response = client.post('/contacto/submit/', data)
    assert response.status_code == 200
    assert Lead.objects.filter(email='test@example.com').exists()
```

**Ejecutar tests:**

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=apps --cov-report=html

# Ver reporte
open htmlcov/index.html
```

**Objetivo:** 80%+ de cobertura de código.

---

### 2. API REST Completa

**¿Por qué?** Permite integraciones, apps móviles, y automatizaciones.

**Implementación:**

```python
# apps/landing/serializers.py
from rest_framework import serializers
from .models import Servicio, Testimonio, Lead

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'titulo', 'descripcion_corta', 'icono', 'beneficio_clave']

class TestimonioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonio
        fields = ['nombre_cliente', 'cargo', 'empresa', 'texto', 'resultado_clave']

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['nombre', 'email', 'telefono', 'empresa', 'mensaje']
        read_only_fields = ['fecha_creacion']
```

```python
# apps/landing/api_views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Servicio, Testimonio, Lead
from .serializers import ServicioSerializer, TestimonioSerializer, LeadSerializer

class ServicioViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para servicios"""
    queryset = Servicio.objects.filter(activo=True)
    serializer_class = ServicioSerializer

class TestimonioViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para testimonios"""
    queryset = Testimonio.objects.filter(activo=True)
    serializer_class = TestimonioSerializer

class LeadViewSet(viewsets.ModelViewSet):
    """API endpoint para leads"""
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    http_method_names = ['post']  # Solo permitir POST

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Enviar notificación
        lead = serializer.instance
        enviar_email_notificacion(lead)

        return Response(
            {'message': 'Lead creado exitosamente'},
            status=status.HTTP_201_CREATED
        )
```

```python
# apps/landing/urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'servicios', ServicioViewSet)
router.register(r'testimonios', TestimonioViewSet)
router.register(r'leads', LeadViewSet)

urlpatterns = [
    # ... URLs existentes
    path('api/', include(router.urls)),
]
```

**Endpoints disponibles:**

```
GET  /api/servicios/          - Listar servicios
GET  /api/servicios/1/        - Detalle de servicio
GET  /api/testimonios/        - Listar testimonios
POST /api/leads/              - Crear lead
```

**Documentación API:**

```bash
pip install drf-spectacular
```

```python
# settings.py
INSTALLED_APPS += ['drf_spectacular']

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

Acceder a: `http://localhost:8000/api/docs/`

---

### 3. Sistema de Caché Robusto

**¿Por qué?** Reduce carga en base de datos y mejora tiempos de respuesta.

```bash
# Instalar Redis
pip install redis django-redis
```

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Configurar sesiones en Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

**Implementar en vistas:**

```python
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60 * 15)  # Cache por 15 minutos
def index(request):
    # Vista se cachea completamente
    pass

def servicios_cached():
    """Cachear query de servicios"""
    servicios = cache.get('servicios_activos')
    if servicios is None:
        servicios = list(Servicio.objects.filter(activo=True).values())
        cache.set('servicios_activos', servicios, 60 * 60)  # 1 hora
    return servicios
```

**Invalidar caché cuando cambia contenido:**

```python
# apps/landing/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Servicio

@receiver([post_save, post_delete], sender=Servicio)
def invalidate_servicios_cache(sender, **kwargs):
    """Limpiar caché cuando cambian servicios"""
    cache.delete('servicios_activos')
```

---

### 4. Internacionalización (i18n)

**¿Por qué?** Permite ofrecer la landing en múltiples idiomas.

```python
# settings.py
LANGUAGE_CODE = 'es'
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
    ('pt', 'Português'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

MIDDLEWARE = [
    # ...
    'django.middleware.locale.LocaleMiddleware',  # Agregar
]
```

**Marcar textos para traducción:**

```html
{% load i18n %}

<h1>{% trans "Transforma el Caos en Claridad" %}</h1>
<p>{% trans "Consultoría estratégica para PYMEs" %}</p>
```

```python
# En código Python
from django.utils.translation import gettext as _

def mi_vista(request):
    mensaje = _("Mensaje enviado exitosamente")
    return HttpResponse(mensaje)
```

**Generar archivos de traducción:**

```bash
# Crear archivos .po
python manage.py makemessages -l en
python manage.py makemessages -l pt

# Traducir en locale/en/LC_MESSAGES/django.po
# Compilar traducciones
python manage.py compilemessages
```

**Selector de idioma en navbar:**

```html
<form action="{% url 'set_language' %}" method="post">
    {% csrf_token %}
    <select name="language" onchange="this.form.submit()">
        <option value="es" {% if LANGUAGE_CODE == 'es' %}selected{% endif %}>🇻🇪 ES</option>
        <option value="en" {% if LANGUAGE_CODE == 'en' %}selected{% endif %}>🇺🇸 EN</option>
        <option value="pt" {% if LANGUAGE_CODE == 'pt' %}selected{% endif %}>🇧🇷 PT</option>
    </select>
</form>
```

---

### 5. Sistema de Versiones de Contenido

**¿Por qué?** Permite revertir cambios y auditar modificaciones.

```bash
pip install django-reversion
```

```python
# settings.py
INSTALLED_APPS += ['reversion']

# apps/landing/models.py
import reversion

@reversion.register()
class Servicio(models.Model):
    # ... campos
    pass

@reversion.register()
class ConfiguracionSitio(SingletonModel):
    # ... campos
    pass
```

**En el admin:**

```python
from reversion.admin import VersionAdmin

@admin.register(Servicio)
class ServicioAdmin(VersionAdmin):
    """Admin con historial de versiones"""
    pass
```

**Revertir cambios:**

```python
from reversion.models import Version

# Ver historial
versions = Version.objects.get_for_object(servicio)

# Revertir a versión anterior
version = versions[1]  # Segunda versión más reciente
version.revert()
```

---

## 💼 Mejoras de Negocio

### 1. CRM Integrado

**¿Por qué?** Gestionar todo el ciclo de vida del cliente en un solo lugar.

**Opciones:**

#### Opción A: Integrar con CRM Externo

```bash
# HubSpot
pip install hubspot-api-client

# Salesforce
pip install simple-salesforce

# Pipedrive
pip install pipedrive-python-lib
```

**Ejemplo con HubSpot:**

```python
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput

def crear_contacto_hubspot(lead):
    """Sincronizar lead con HubSpot"""
    client = HubSpot(access_token=settings.HUBSPOT_API_KEY)

    contact_data = SimplePublicObjectInput(
        properties={
            "email": lead.email,
            "firstname": lead.nombre.split()[0],
            "lastname": " ".join(lead.nombre.split()[1:]),
            "phone": lead.telefono,
            "company": lead.empresa,
            "message": lead.mensaje,
        }
    )

    try:
        response = client.crm.contacts.basic_api.create(
            simple_public_object_input=contact_data
        )
        lead.hubspot_id = response.id
        lead.save()
    except Exception as e:
        logger.error(f"Error al crear contacto en HubSpot: {e}")
```

**Llamar después de crear lead:**

```python
def contacto_submit(request):
    # ... crear lead
    crear_contacto_hubspot(lead)  # Sincronizar
    # ...
```

#### Opción B: CRM Simple Integrado

```python
# apps/crm/models.py
class Pipeline(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.IntegerField()

class Etapa(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    orden = models.IntegerField()
    probabilidad = models.IntegerField(help_text="% de cierre")

class Oportunidad(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    etapa = models.ForeignKey(Etapa, on_delete=models.SET_NULL, null=True)
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_cierre_estimada = models.DateField()
    probabilidad = models.IntegerField()

    # Actividades
    ultima_actividad = models.DateTimeField(auto_now=True)
    proxima_actividad = models.DateTimeField(null=True, blank=True)

    def calcular_valor_ponderado(self):
        """Valor * probabilidad"""
        return self.valor_estimado * (self.probabilidad / 100)

class Actividad(models.Model):
    TIPO_CHOICES = [
        ('llamada', 'Llamada'),
        ('email', 'Email'),
        ('reunion', 'Reunión'),
        ('whatsapp', 'WhatsApp'),
    ]

    oportunidad = models.ForeignKey(Oportunidad, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
```

**Dashboard de ventas:**

```python
def dashboard_ventas(request):
    """Dashboard CRM con métricas clave"""

    # Total de oportunidades por etapa
    oportunidades_por_etapa = Oportunidad.objects.values(
        'etapa__nombre'
    ).annotate(
        total=Count('id'),
        valor_total=Sum('valor_estimado'),
        valor_ponderado=Sum(
            F('valor_estimado') * F('probabilidad') / 100
        )
    )

    # Leads sin seguimiento (>7 días sin actividad)
    leads_frios = Lead.objects.filter(
        ultima_actividad__lt=timezone.now() - timedelta(days=7),
        estado='contactado'
    )

    # Tasa de conversión
    total_leads = Lead.objects.count()
    leads_convertidos = Oportunidad.objects.filter(
        etapa__nombre='Ganado'
    ).count()
    tasa_conversion = (leads_convertidos / total_leads * 100) if total_leads > 0 else 0

    context = {
        'oportunidades_por_etapa': oportunidades_por_etapa,
        'leads_frios': leads_frios,
        'tasa_conversion': tasa_conversion,
    }

    return render(request, 'crm/dashboard.html', context)
```

---

### 2. Sistema de Cotizaciones Automáticas

**¿Por qué?** Acelera el proceso de ventas y mejora la experiencia del cliente.

```python
# apps/cotizaciones/models.py
class PaqueteServicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    servicios = models.ManyToManyField(Servicio)
    duracion_estimada = models.CharField(max_length=100)

class Cotizacion(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('enviada', 'Enviada'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    paquete = models.ForeignKey(PaqueteServicio, on_delete=models.SET_NULL, null=True)

    # Personalización
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    condiciones = models.TextField()

    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField()

    # URL única para aceptar/rechazar
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def generar_pdf(self):
        """Generar PDF de cotización"""
        # Usar reportlab o weasyprint
        pass
```

**Vista pública para aceptar cotización:**

```python
def cotizacion_publica(request, uuid):
    """Vista para que el cliente revise y acepte cotización"""
    cotizacion = get_object_or_404(Cotizacion, uuid=uuid)

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'aceptar':
            cotizacion.estado = 'aceptada'
            cotizacion.save()

            # Crear oportunidad en etapa "Ganado"
            Oportunidad.objects.create(
                lead=cotizacion.lead,
                valor_estimado=cotizacion.precio_final,
                etapa=Etapa.objects.get(nombre='Ganado')
            )

            # Enviar confirmación
            enviar_email_aceptacion(cotizacion)

            return redirect('cotizacion_gracias')

        elif accion == 'rechazar':
            motivo = request.POST.get('motivo')
            cotizacion.estado = 'rechazada'
            cotizacion.save()

            # Notificar al equipo
            notificar_rechazo(cotizacion, motivo)

    return render(request, 'cotizaciones/publica.html', {'cotizacion': cotizacion})
```

---

### 3. Portal de Clientes

**¿Por qué?** Mejora la transparencia y reduce consultas repetitivas.

```python
# apps/clientes/models.py
class Cliente(models.Model):
    """Extensión del Lead cuando se convierte en cliente"""
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    # Información adicional
    fecha_conversion = models.DateTimeField(auto_now_add=True)
    nit_rif = models.CharField(max_length=50)
    direccion_fiscal = models.TextField()

class Proyecto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20)
    progreso = models.IntegerField(default=0)  # 0-100%

class EntregableProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='entregables/')
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

class Ticket(models.Model):
    """Sistema de soporte"""
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES)
    estado = models.CharField(max_length=20, default='abierto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

**Dashboard del cliente:**

```python
@login_required
def cliente_dashboard(request):
    """Dashboard para clientes"""
    cliente = request.user.cliente

    proyectos_activos = Proyecto.objects.filter(
        cliente=cliente,
        estado='activo'
    )

    tickets_abiertos = Ticket.objects.filter(
        cliente=cliente,
        estado='abierto'
    )

    ultimos_entregables = EntregableProyecto.objects.filter(
        proyecto__cliente=cliente
    ).order_by('-fecha_entrega')[:5]

    context = {
        'proyectos': proyectos_activos,
        'tickets': tickets_abiertos,
        'entregables': ultimos_entregables,
    }

    return render(request, 'clientes/dashboard.html', context)
```

---

### 4. Sistema de Referidos

**¿Por qué?** El marketing boca a boca es el más efectivo y económico.

```python
# apps/referidos/models.py
class ProgramaReferidos(SingletonModel):
    activo = models.BooleanField(default=True)
    comision_porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    comision_fija = models.DecimalField(max_digits=10, decimal_places=2)
    beneficio_referido = models.CharField(max_length=200)  # ej: "15% descuento"

class CodigoReferido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20, unique=True)

    # Métricas
    veces_usado = models.IntegerField(default=0)
    comision_acumulada = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def generar_codigo(self):
        """Generar código único"""
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class ReferidoUsado(models.Model):
    codigo = models.ForeignKey(CodigoReferido, on_delete=models.CASCADE)
    lead_referido = models.ForeignKey(Lead, on_delete=models.CASCADE)
    fecha_uso = models.DateTimeField(auto_now_add=True)
    convertido = models.BooleanField(default=False)
    comision_pagada = models.BooleanField(default=False)
```

**En el formulario de contacto:**

```html
<input type="text"
       name="codigo_referido"
       placeholder="¿Tienes un código de referido?"
       class="form-input">
```

```python
def contacto_submit(request):
    # ... crear lead

    codigo_referido = request.POST.get('codigo_referido')
    if codigo_referido:
        try:
            codigo = CodigoReferido.objects.get(codigo=codigo_referido.upper())
            ReferidoUsado.objects.create(
                codigo=codigo,
                lead_referido=lead
            )
            codigo.veces_usado += 1
            codigo.save()

            # Aplicar beneficio al lead
            lead.descuento_aplicado = 15  # 15%
            lead.save()

        except CodigoReferido.DoesNotExist:
            pass

    # ...
```

---

## 🏗️ Escalabilidad y Arquitectura

### 1. Microservicios (Futuro)

**¿Cuándo?** Cuando tengas +100 landing pages o +10,000 leads/mes.

**Arquitectura sugerida:**

```
┌─────────────────┐
│   API Gateway   │  ← Entrada única (Kong, AWS API Gateway)
└────────┬────────┘
         │
    ┌────┴────┬─────────┬──────────┐
    │         │         │          │
┌───▼───┐ ┌──▼───┐ ┌───▼────┐ ┌───▼────┐
│Landing│ │ CRM  │ │Analytics│ │Payments│
│Service│ │Service│ │ Service│ │Service │
└───┬───┘ └──┬───┘ └───┬────┘ └───┬────┘
    │        │         │          │
    └────────┴─────────┴──────────┘
             │
       ┌─────▼──────┐
       │  PostgreSQL│
       │   (Master) │
       └─────┬──────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼───┐
│Replica1│      │Replica2│
└────────┘      └────────┘
```

**Tecnologías:**

- **API Gateway:** Kong, AWS API Gateway
- **Service Mesh:** Istio (avanzado)
- **Message Queue:** RabbitMQ, AWS SQS
- **Cache:** Redis Cluster
- **DB:** PostgreSQL con replicación

---

### 2. Multi-Tenancy

**¿Por qué?** Permite ofrecer SaaS a otras empresas.

**Estrategias:**

#### A. Schema por Tenant (Mejor aislamiento)

```python
# Usar django-tenants
pip install django-tenants

# settings.py
SHARED_APPS = [
    'django_tenants',
    'django.contrib.admin',
    # Apps compartidas
]

TENANT_APPS = [
    'apps.landing',  # Cada tenant tiene su propia landing
    'apps.crm',      # Y su propio CRM
]

TENANT_MODEL = "tenants.Tenant"
TENANT_DOMAIN_MODEL = "tenants.Domain"
```

```python
# apps/tenants/models.py
from django_tenants.models import TenantMixin, DomainMixin

class Tenant(TenantMixin):
    nombre = models.CharField(max_length=100)
    plan = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Domain(DomainMixin):
    pass
```

**Resultado:**
- cliente1.tudominio.com → Schema `cliente1`
- cliente2.tudominio.com → Schema `cliente2`
- Aislamiento completo de datos

#### B. Foreign Key Compartido (Más simple)

```python
class Empresa(models.Model):
    """Cada empresa/cliente es un tenant"""
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    plan = models.CharField(max_length=50)

class Lead(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)  # Filtrar por empresa
    nombre = models.CharField(max_length=200)
    # ... campos

    class Meta:
        indexes = [
            models.Index(fields=['empresa', 'fecha_creacion']),
        ]
```

```python
# Middleware para filtrar por tenant
class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener empresa del subdominio
        host = request.get_host()
        subdomain = host.split('.')[0]

        try:
            empresa = Empresa.objects.get(slug=subdomain)
            request.empresa = empresa
        except Empresa.DoesNotExist:
            return HttpResponse('Empresa no encontrada', status=404)

        return self.get_response(request)
```

---

### 3. CDN y Optimización de Assets

**¿Por qué?** Reduce tiempos de carga globalmente.

**Implementar con Cloudflare (Gratis):**

1. Crear cuenta en Cloudflare
2. Agregar tu dominio
3. Cambiar nameservers en tu registrar
4. Configurar:
   - Auto minify (CSS, JS, HTML)
   - Brotli compression
   - Always use HTTPS
   - Cache level: Standard

**O usar AWS CloudFront:**

```python
# settings.py
# Después de collectstatic, subir a S3

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'smartsolutions-static'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Usar S3 para archivos estáticos
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Configurar CloudFront delante de S3
CLOUDFRONT_DOMAIN = 'dxxxx.cloudfront.net'
STATIC_URL = f'https://{CLOUDFRONT_DOMAIN}/static/'
```

---

## 🎯 SEO y Marketing Digital

### 1. SEO On-Page Avanzado

```python
# apps/core/models.py
class SEOConfig(models.Model):
    """Configuración SEO por página"""
    pagina = models.CharField(max_length=50, unique=True)

    # Meta tags
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=160)
    keywords = models.CharField(max_length=200)

    # Open Graph
    og_title = models.CharField(max_length=60)
    og_description = models.CharField(max_length=160)
    og_image = models.ImageField(upload_to='seo/')

    # Twitter Card
    twitter_card_type = models.CharField(max_length=20, default='summary_large_image')

    # Schema.org (JSON-LD)
    schema_json = models.JSONField(blank=True, null=True)

    # Canonical URL
    canonical_url = models.URLField(blank=True)
```

**Template SEO:**

```html
<!-- templates/base.html -->
{% block seo %}
    <!-- Title -->
    <title>{{ seo.title|default:config.meta_titulo }}</title>

    <!-- Meta Description -->
    <meta name="description" content="{{ seo.description|default:config.meta_descripcion }}">

    <!-- Canonical -->
    {% if seo.canonical_url %}
        <link rel="canonical" href="{{ seo.canonical_url }}">
    {% endif %}

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{{ seo.og_title|default:seo.title }}">
    <meta property="og:description" content="{{ seo.og_description|default:seo.description }}">
    <meta property="og:image" content="{{ seo.og_image.url|default:'/static/img/og-default.jpg' }}">
    <meta property="og:url" content="{{ request.build_absolute_uri }}">

    <!-- Schema.org -->
    {% if seo.schema_json %}
        <script type="application/ld+json">
            {{ seo.schema_json|safe }}
        </script>
    {% endif %}
{% endblock %}
```

**Schema.org para Organización:**

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "SmartSolutions VE",
  "url": "https://smartsolutions.ve",
  "logo": "https://smartsolutions.ve/static/img/logo.png",
  "description": "Consultoría estratégica para PYMEs venezolanas",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Valencia",
    "addressRegion": "Carabobo",
    "addressCountry": "VE"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+58-412-169-1851",
    "contactType": "Sales",
    "email": "contacto@smartsolutions.ve"
  },
  "sameAs": [
    "https://linkedin.com/company/smartsolutions-ve",
    "https://instagram.com/smartsolutions.ve"
  ]
}
```

**Sitemap dinámico:**

```python
from django.contrib.sitemaps import Sitemap
from .models import Servicio, Caso

class ServicioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Servicio.objects.filter(activo=True)

    def lastmod(self, obj):
        return obj.fecha_actualizacion

# urls.py
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'servicios': ServicioSitemap,
}

urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]
```

---

### 2. Marketing Automation

**A. Email Marketing con Mailchimp:**

```bash
pip install mailchimp-marketing
```

```python
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

def agregar_a_mailchimp(lead):
    """Agregar lead a lista de Mailchimp"""
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": settings.MAILCHIMP_API_KEY,
        "server": "us1"  # Tu servidor
    })

    try:
        response = client.lists.add_list_member(
            settings.MAILCHIMP_LIST_ID,
            {
                "email_address": lead.email,
                "status": "subscribed",
                "merge_fields": {
                    "FNAME": lead.nombre.split()[0],
                    "LNAME": " ".join(lead.nombre.split()[1:]),
                    "PHONE": lead.telefono,
                    "COMPANY": lead.empresa,
                }
            }
        )
        return response
    except ApiClientError as error:
        logger.error(f"Error Mailchimp: {error.text}")
```

**Secuencia de emails automatizada:**

```
Lead llena formulario
    ↓
Email 1 (Inmediato): Bienvenida + Recurso gratuito
    ↓
Email 2 (Día 2): Caso de éxito relevante
    ↓
Email 3 (Día 5): Oferta especial con descuento
    ↓
Email 4 (Día 10): Recordatorio + Testimonios
```

**B. Chatbot con Tidio/Drift:**

```html
<!-- templates/base.html -->
<!-- Tidio Chat Widget -->
<script src="//code.tidio.co/tu-codigo-unico.js" async></script>
```

**Automatizar respuestas:**
- "¿Cuánto cuesta?" → Enviar link a cotización
- "¿Qué servicios ofrecen?" → Mostrar servicios
- Horario no laboral → "Te responderemos en X horas"

---

### 3. Pixel Tracking y Retargeting

**Facebook Pixel:**

```html
<!-- templates/base.html -->
<!-- Facebook Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'TU_PIXEL_ID');
fbq('track', 'PageView');
</script>
```

**Eventos personalizados:**

```html
<!-- En formulario de contacto -->
<script>
    document.getElementById('contacto-form').addEventListener('submit', function() {
        fbq('track', 'Lead', {
            content_name: 'Formulario Contacto',
            content_category: 'Lead Generation'
        });
    });
</script>
```

**Google Tag Manager:**

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->
```

Gestionar todos los pixels desde GTM (Facebook, Google Ads, LinkedIn, etc.)

---

Continúa en la siguiente parte... (Character limit alcanzado)
