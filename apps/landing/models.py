from django.db import models


class Servicio(models.Model):
    """Servicios que ofrece SmartSolutions VE — editables desde el admin."""

    ICONOS = [
        ('chart-bar', '📊 Analytics / Dashboard'),
        ('cog', '⚙️ Automatización'),
        ('device-mobile', '📱 App / Software'),
        ('database', '🗄️ Base de Datos'),
        ('lightning-bolt', '⚡ Optimización'),
        ('presentation-chart-line', '📈 Consultoría'),
        ('cube', '🧩 Integración'),
        ('shield-check', '🛡️ Seguridad'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion_corta = models.CharField(
        max_length=200,
        help_text="Una línea que resume el servicio (aparece en la card)"
    )
    descripcion_larga = models.TextField(
        help_text="Descripción detallada (opcional, para modal o página de detalle)",
        blank=True
    )
    icono = models.CharField(max_length=50, choices=ICONOS, default='cog')
    beneficio_clave = models.CharField(
        max_length=100,
        help_text="Ej: 'Reduce errores en un 80%'",
        blank=True
    )
    orden = models.PositiveSmallIntegerField(default=0, help_text="Orden de aparición (menor = primero)")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['orden', 'titulo']

    def __str__(self):
        return self.titulo


class Testimonio(models.Model):
    """Testimonios de clientes — con foto y métricas opcionales."""

    nombre_cliente = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True, help_text="Ej: Gerente General")
    empresa = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=100, blank=True, help_text="Ej: Distribuidora, Farmacia...")
    foto = models.ImageField(
        upload_to='testimonios/',
        blank=True,
        null=True,
        help_text="Foto del cliente (opcional)"
    )
    texto = models.TextField(help_text="El testimonio en sus propias palabras")
    resultado_clave = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ej: '+40% en ventas en 60 días'"
    )
    orden = models.PositiveSmallIntegerField(default=0)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(
        default=False,
        help_text="Los testimonios destacados aparecen primero y más prominentes"
    )

    class Meta:
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"
        ordering = ['-destacado', 'orden']

    def __str__(self):
        return f"{self.nombre_cliente} — {self.empresa}"


class CasoDeExito(models.Model):
    """Casos de éxito con métricas cuantificables."""

    titulo = models.CharField(max_length=150)
    empresa = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    descripcion = models.TextField(help_text="Describe el problema que tenían y cómo lo resolvieron")

    # Métricas (hasta 3)
    metrica_1_valor = models.CharField(max_length=30, blank=True, help_text="Ej: +65%")
    metrica_1_label = models.CharField(max_length=60, blank=True, help_text="Ej: Reducción de costos operativos")
    metrica_2_valor = models.CharField(max_length=30, blank=True)
    metrica_2_label = models.CharField(max_length=60, blank=True)
    metrica_3_valor = models.CharField(max_length=30, blank=True)
    metrica_3_label = models.CharField(max_length=60, blank=True)

    imagen = models.ImageField(upload_to='casos/', blank=True, null=True)
    orden = models.PositiveSmallIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Caso de Éxito"
        verbose_name_plural = "Casos de Éxito"
        ordering = ['orden']

    def __str__(self):
        return f"{self.titulo} ({self.empresa})"

    @property
    def metricas(self):
        """Retorna lista de métricas no vacías."""
        result = []
        for i in range(1, 4):
            valor = getattr(self, f'metrica_{i}_valor')
            label = getattr(self, f'metrica_{i}_label')
            if valor and label:
                result.append({'valor': valor, 'label': label})
        return result


class Lead(models.Model):
    """
    Registro de contactos desde el formulario de la landing.
    Cada envío del formulario crea un Lead en la base de datos.
    """

    ESTADOS = [
        ('nuevo', 'Nuevo'),
        ('contactado', 'Contactado'),
        ('en_proceso', 'En Proceso'),
        ('cerrado', 'Cerrado'),
        ('descartado', 'Descartado'),
    ]

    SERVICIOS_INTERES = [
        ('automatizacion', 'Automatización de Procesos'),
        ('dashboard', 'Dashboard / BI'),
        ('software', 'Software a Medida'),
        ('consultoria', 'Consultoría Tecnológica'),
        ('otro', 'Otro'),
    ]

    # Datos del contacto
    nombre = models.CharField(max_length=150)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)
    empresa = models.CharField(max_length=150, blank=True)
    servicio_interes = models.CharField(
        max_length=50,
        choices=SERVICIOS_INTERES,
        blank=True,
        default='otro'
    )
    mensaje = models.TextField()

    # Gestión interna
    estado = models.CharField(max_length=20, choices=ESTADOS, default='nuevo')
    notas_internas = models.TextField(
        blank=True,
        help_text="Notas privadas del equipo (no visibles para el cliente)"
    )

    # Metadata
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    ip_origen = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = "Lead / Contacto"
        verbose_name_plural = "Leads / Contactos"
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.nombre} ({self.email}) — {self.get_estado_display()}"
