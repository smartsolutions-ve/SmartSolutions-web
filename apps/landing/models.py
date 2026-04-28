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


# ─────────────────────────────────────────
# SISTEMA DE FORMULARIOS DINÁMICOS
# ─────────────────────────────────────────

class Formulario(models.Model):
    """
    Formulario de levantamiento de información configurable desde el admin.
    Puede tener múltiples fases, cada una con sus propias preguntas.
    """
    nombre = models.CharField(max_length=150, help_text="Nombre interno del formulario")
    slug = models.SlugField(
        unique=True,
        help_text="URL amigable: diagnostico-empresarial → /formulario/diagnostico-empresarial/"
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción visible para el usuario al inicio del formulario"
    )
    activo = models.BooleanField(default=True)
    es_principal = models.BooleanField(
        default=False,
        help_text="Si está activo, este formulario reemplaza el formulario de contacto en la landing page"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Formulario"
        verbose_name_plural = "Formularios"
        ordering = ['-es_principal', 'nombre']

    def __str__(self):
        return f"{self.nombre}{'  [PRINCIPAL]' if self.es_principal else ''}"

    @property
    def fases_activas(self):
        return self.fases.order_by('orden')


class FaseFormulario(models.Model):
    """Una fase/paso dentro de un formulario."""
    formulario = models.ForeignKey(
        Formulario, on_delete=models.CASCADE, related_name='fases'
    )
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(
        blank=True,
        help_text="Texto explicativo que verá el usuario en esta fase"
    )
    orden = models.PositiveSmallIntegerField(default=0)
    icono = models.CharField(
        max_length=10, blank=True,
        help_text="Emoji o código de icono (ej: 🏢, 📊)"
    )

    class Meta:
        verbose_name = "Fase del Formulario"
        verbose_name_plural = "Fases del Formulario"
        ordering = ['orden']

    def __str__(self):
        return f"[{self.formulario.nombre}] Fase {self.orden}: {self.titulo}"

    @property
    def preguntas_activas(self):
        return self.preguntas.order_by('orden')


class PreguntaFormulario(models.Model):
    """Una pregunta/campo dentro de una fase de un formulario."""

    TIPOS_CAMPO = [
        ('text', 'Texto corto'),
        ('email', 'Email'),
        ('tel', 'Teléfono'),
        ('number', 'Número'),
        ('textarea', 'Texto largo'),
        ('select', 'Lista desplegable'),
        ('radio', 'Opción única (radio)'),
        ('checkbox', 'Opción múltiple (checkbox)'),
        ('date', 'Fecha'),
    ]

    ANCHOS = [
        ('full', 'Ancho completo (100%)'),
        ('half', 'Medio ancho (50%)'),
    ]

    fase = models.ForeignKey(
        FaseFormulario, on_delete=models.CASCADE, related_name='preguntas'
    )
    tipo_campo = models.CharField(max_length=20, choices=TIPOS_CAMPO, default='text')
    etiqueta = models.CharField(max_length=200, help_text="Texto del label visible")
    placeholder = models.CharField(max_length=200, blank=True)
    texto_ayuda = models.CharField(
        max_length=300, blank=True,
        help_text="Texto de ayuda debajo del campo"
    )
    requerido = models.BooleanField(default=True)
    opciones = models.TextField(
        blank=True,
        help_text="Solo para select/radio/checkbox. Una opción por línea."
    )
    ancho = models.CharField(max_length=10, choices=ANCHOS, default='full')
    orden = models.PositiveSmallIntegerField(default=0)

    # Lógica condicional
    condicion_pregunta = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='dependientes',
        help_text="Mostrar esta pregunta solo si la respuesta a OTRA pregunta cumple una condición"
    )
    condicion_valor = models.CharField(
        max_length=200, blank=True,
        help_text="Valor exacto que debe tener la respuesta de la pregunta condicional"
    )

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ['orden']

    def __str__(self):
        return f"{self.etiqueta} ({self.get_tipo_campo_display()})"

    def get_opciones_list(self):
        """Retorna las opciones como lista de tuplas (valor, label)."""
        if not self.opciones:
            return []
        lineas = [l.strip() for l in self.opciones.strip().splitlines() if l.strip()]
        return [(l, l) for l in lineas]


class SesionFormulario(models.Model):
    """
    Registro de un usuario que está completando (o completó) un formulario.
    Almacena el estado de avance entre fases.
    """
    formulario = models.ForeignKey(
        Formulario, on_delete=models.CASCADE, related_name='sesiones'
    )
    lead = models.ForeignKey(
        Lead, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='sesiones_formulario'
    )
    fase_actual = models.PositiveSmallIntegerField(default=1)
    completado = models.BooleanField(default=False)
    ip_origen = models.GenericIPAddressField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sesión / Respuesta Recibida"
        verbose_name_plural = "Sesiones / Respuestas Recibidas"
        ordering = ['-creado_en']

    def __str__(self):
        estado = '✅ Completada' if self.completado else f'⏳ Fase {self.fase_actual}'
        nombre = self.lead.nombre if self.lead else 'Anónimo'
        return f"{self.formulario.nombre} — {nombre} ({estado})"

    def get_respuestas_agrupadas(self):
        """Retorna respuestas agrupadas por fase para email/admin."""
        resultado = []
        for fase in self.formulario.fases_activas:
            respuestas_fase = self.respuestas.filter(
                pregunta__fase=fase
            ).select_related('pregunta').order_by('pregunta__orden')
            if respuestas_fase.exists():
                resultado.append({
                    'fase': fase,
                    'respuestas': respuestas_fase,
                })
        return resultado


class RespuestaFormulario(models.Model):
    """Una respuesta individual a una pregunta de un formulario."""
    sesion = models.ForeignKey(
        SesionFormulario, on_delete=models.CASCADE, related_name='respuestas'
    )
    pregunta = models.ForeignKey(
        PreguntaFormulario, on_delete=models.CASCADE, related_name='respuestas'
    )
    valor = models.TextField(blank=True)

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"
        unique_together = [('sesion', 'pregunta')]

    def __str__(self):
        return f"{self.pregunta.etiqueta}: {self.valor[:60]}"
