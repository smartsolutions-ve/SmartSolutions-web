from django.db import models


class ConfiguracionSitio(models.Model):
    """
    Configuración global del sitio. Solo debe existir UN registro.
    Se edita desde el admin y se inyecta en todos los templates via context_processor.
    """
    # Identidad
    nombre_empresa = models.CharField(max_length=100, default="SmartSolutions VE")
    slogan = models.CharField(max_length=200, default="Procesos Alineados, Decisiones Inteligentes")
    descripcion_corta = models.TextField(
        max_length=300,
        default="Transformamos PYMEs venezolanas con tecnología, automatización y estrategia de datos."
    )

    # Contacto
    email_contacto = models.EmailField(default="contacto@smartsolutions.com.ve")
    whatsapp_numero = models.CharField(
        max_length=20,
        default="+58 412 0000000",
        help_text="Formato: +58XXXXXXXXXX (sin espacios para el link)"
    )
    whatsapp_mensaje = models.CharField(
        max_length=300,
        default="Hola, me interesa conocer más sobre sus servicios.",
        help_text="Mensaje pre-cargado al hacer clic en el botón de WhatsApp"
    )

    # Redes sociales
    linkedin_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    facebook_url = models.URLField(blank=True, default="")

    # SEO
    meta_titulo = models.CharField(
        max_length=70,
        default="SmartSolutions VE | Consultoría Tecnológica para PYMEs"
    )
    meta_descripcion = models.CharField(
        max_length=160,
        default="Ayudamos a PYMEs venezolanas a crecer con automatización, datos y tecnología a medida."
    )

    # Hero section
    hero_titulo_principal = models.CharField(
        max_length=100,
        default="Aumenta la Rentabilidad de tu PYME"
    )
    hero_titulo_acento = models.CharField(
        max_length=60,
        default="en 90 días o menos"
    )
    hero_subtitulo = models.TextField(
        max_length=300,
        default="Sin datos confiables, cada decisión es una apuesta. Te ayudamos a convertir la incertidumbre en crecimiento predecible."
    )

    # Métricas del hero
    metrica_1_valor = models.CharField(max_length=20, default="+50")
    metrica_1_label = models.CharField(max_length=50, default="PYMEs transformadas")
    metrica_2_valor = models.CharField(max_length=20, default="+200%")
    metrica_2_label = models.CharField(max_length=50, default="Mejora en eficiencia")
    metrica_3_valor = models.CharField(max_length=20, default="90 días")
    metrica_3_label = models.CharField(max_length=50, default="Tiempo al primer resultado")

    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuración del Sitio"

    def __str__(self):
        return self.nombre_empresa

    def save(self, *args, **kwargs):
        # Singleton: solo permite un registro
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
