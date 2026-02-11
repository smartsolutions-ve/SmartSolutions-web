from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ConfiguracionSitio


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(ModelAdmin):
    fieldsets = (
        ("🏢 Identidad de la Empresa", {
            "fields": ("nombre_empresa", "slogan", "descripcion_corta"),
        }),
        ("📞 Contacto y WhatsApp", {
            "fields": ("email_contacto", "whatsapp_numero", "whatsapp_mensaje"),
        }),
        ("📱 Redes Sociales", {
            "fields": ("linkedin_url", "instagram_url", "twitter_url", "facebook_url"),
            "classes": ["collapse"],
        }),
        ("🔍 SEO", {
            "fields": ("meta_titulo", "meta_descripcion"),
        }),
        ("🦸 Hero Section", {
            "fields": (
                "hero_titulo_principal",
                "hero_titulo_acento",
                "hero_subtitulo",
            ),
        }),
        ("📊 Métricas del Hero", {
            "fields": (
                ("metrica_1_valor", "metrica_1_label"),
                ("metrica_2_valor", "metrica_2_label"),
                ("metrica_3_valor", "metrica_3_label"),
            ),
        }),
    )

    def has_add_permission(self, request):
        # Singleton: no permitir crear más de uno
        return not ConfiguracionSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
