from .models import ConfiguracionSitio


def site_config(request):
    """
    Inyecta la configuración global del sitio en todos los templates.
    Uso en template: {{ config.nombre_empresa }}, {{ config.whatsapp_numero }}, etc.
    """
    return {
        'config': ConfiguracionSitio.get_config()
    }
