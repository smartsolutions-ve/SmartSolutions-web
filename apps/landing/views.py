import resend
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from apps.core.models import ConfiguracionSitio
from .models import Servicio, Testimonio, CasoDeExito
from .forms import ContactoForm


def landing(request):
    """Vista principal de la landing page."""
    context = {
        'servicios': Servicio.objects.filter(activo=True),
        'testimonios': Testimonio.objects.filter(activo=True),
        'casos': CasoDeExito.objects.filter(activo=True),
        'form': ContactoForm(),
    }
    return render(request, 'landing/index.html', context)


@require_http_methods(["POST"])
def contacto_submit(request):
    """
    Procesa el formulario de contacto:
    1. Valida los datos
    2. Guarda el Lead en BD
    3. Envía email de notificación via Resend
    4. Retorna respuesta (JSON para HTMX, redirect para fallback)
    """
    form = ContactoForm(request.POST)
    is_htmx = request.headers.get('HX-Request') == 'true'

    if form.is_valid():
        # Guardar el lead
        lead = form.save(commit=False)
        # Capturar IP
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            lead.ip_origen = ip.split(',')[0].strip()
        else:
            lead.ip_origen = request.META.get('REMOTE_ADDR')
        lead.save()

        # Enviar email de notificación
        _enviar_email_notificacion(lead)

        if is_htmx:
            return render(request, 'components/contacto_success.html', {'lead': lead})

        messages.success(request, '¡Mensaje enviado! Te contactaremos pronto.')
        return redirect('landing:index')

    # Formulario inválido
    if is_htmx:
        return render(request, 'components/contacto_form.html', {'form': form}, status=422)

    # Fallback sin HTMX
    config = ConfiguracionSitio.get_config()
    context = {
        'servicios': Servicio.objects.filter(activo=True),
        'testimonios': Testimonio.objects.filter(activo=True),
        'casos': CasoDeExito.objects.filter(activo=True),
        'form': form,
    }
    return render(request, 'landing/index.html', context, status=422)


def _enviar_email_notificacion(lead):
    """Envía email de notificación al equipo de SmartSolutions."""
    if not settings.RESEND_API_KEY:
        return  # En desarrollo, no enviar emails

    resend.api_key = settings.RESEND_API_KEY

    html_content = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #0066FF; padding: 20px; border-radius: 8px 8px 0 0;">
            <h1 style="color: white; margin: 0; font-size: 20px;">
                🔔 Nuevo Lead — SmartSolutions VE
            </h1>
        </div>
        <div style="background: #f9f9f9; padding: 24px; border-radius: 0 0 8px 8px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; color: #333; width: 140px;">Nombre:</td>
                    <td style="padding: 8px 0; color: #555;">{lead.nombre}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; color: #333;">Email:</td>
                    <td style="padding: 8px 0; color: #555;">
                        <a href="mailto:{lead.email}">{lead.email}</a>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; color: #333;">Teléfono:</td>
                    <td style="padding: 8px 0; color: #555;">{lead.telefono or '—'}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; color: #333;">Empresa:</td>
                    <td style="padding: 8px 0; color: #555;">{lead.empresa or '—'}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; color: #333;">Servicio:</td>
                    <td style="padding: 8px 0; color: #555;">{lead.get_servicio_interes_display()}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; color: #333; vertical-align: top;">Mensaje:</td>
                    <td style="padding: 8px 0; color: #555;">{lead.mensaje}</td>
                </tr>
            </table>

            <div style="margin-top: 24px; padding: 16px; background: white; border-radius: 6px; border-left: 4px solid #0066FF;">
                <a href="{settings.SITE_URL}/admin/landing/lead/{lead.pk}/change/"
                   style="color: #0066FF; text-decoration: none; font-weight: bold;">
                    → Ver en el Admin Panel
                </a>
            </div>
        </div>
    </div>
    """

    try:
        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [settings.CONTACT_EMAIL],
            "subject": f"[SmartSolutions] Nuevo Lead: {lead.nombre} — {lead.get_servicio_interes_display()}",
            "html": html_content,
        })
    except Exception as e:
        # No fallar si el email falla — el lead ya está en BD
        print(f"Error enviando email: {e}")
