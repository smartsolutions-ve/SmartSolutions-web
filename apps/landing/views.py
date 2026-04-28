import resend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from apps.core.models import ConfiguracionSitio
from .models import (
    Servicio, Testimonio, CasoDeExito,
    Formulario, FaseFormulario, SesionFormulario, RespuestaFormulario, Lead,
)
from .forms import ContactoForm, DynamicPhaseForm
from .utils_pdf import generar_pdf_sesion
from django.http import HttpResponse


def landing(request):
    """Vista principal de la landing page."""
    # Verificar si hay un formulario dinámico principal activo
    formulario_principal = Formulario.objects.filter(activo=True, es_principal=True).first()

    context = {
        'servicios': Servicio.objects.filter(activo=True),
        'testimonios': Testimonio.objects.filter(activo=True),
        'casos': CasoDeExito.objects.filter(activo=True),
        'form': ContactoForm(),
        'formulario_principal': formulario_principal,
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
    context = {
        'servicios': Servicio.objects.filter(activo=True),
        'testimonios': Testimonio.objects.filter(activo=True),
        'casos': CasoDeExito.objects.filter(activo=True),
        'form': form,
    }
    return render(request, 'landing/index.html', context, status=422)


# ──────────────────────────────────────────────────────────
# FORMULARIOS DINÁMICOS
# ──────────────────────────────────────────────────────────

def formulario_inicio(request, slug=None):
    """
    Inicia un formulario dinámico:
    - Si hay slug → carga ese formulario específico
    - Sin slug → redirige al formulario principal si existe
    Crea la SesionFormulario y muestra la fase 1 vía HTMX.
    """
    if slug:
        formulario = get_object_or_404(Formulario, slug=slug, activo=True)
    else:
        formulario = get_object_or_404(Formulario, activo=True, es_principal=True)

    fases = list(formulario.fases_activas)
    if not fases:
        messages.error(request, 'Este formulario no tiene fases configuradas.')
        return redirect('landing:index')

    # Crear sesión
    sesion = SesionFormulario.objects.create(
        formulario=formulario,
        ip_origen=_get_ip(request),
        fase_actual=1,
    )
    # Guardar sesion_id en la sesión HTTP del usuario
    request.session[f'formulario_sesion_{formulario.pk}'] = sesion.pk

    fase = fases[0]
    form = DynamicPhaseForm(fase=fase)

    context = {
        'formulario': formulario,
        'fase': fase,
        'fases': fases,
        'form': form,
        'sesion': sesion,
        'num_fase_actual': 1,
        'total_fases': len(fases),
        'es_ultima_fase': len(fases) == 1,
    }

    is_htmx = request.headers.get('HX-Request') == 'true'
    if is_htmx:
        return render(request, 'components/formulario_fase.html', context)

    return render(request, 'landing/formulario_dinamico.html', context)


@require_http_methods(["POST"])
def formulario_fase(request, sesion_id):
    """
    Procesa el POST de una fase del formulario dinámico.
    - Valida y guarda respuestas de la fase actual
    - Avanza a la siguiente fase (via HTMX) o finaliza el formulario
    """
    sesion = get_object_or_404(SesionFormulario, pk=sesion_id)
    formulario = sesion.formulario
    fases = list(formulario.fases_activas)
    total_fases = len(fases)

    # Obtener la fase actual (1-indexed en el modelo)
    fase_idx = sesion.fase_actual - 1
    if fase_idx >= total_fases:
        return redirect('landing:index')

    fase = fases[fase_idx]

    # Cargar respuestas previas para evaluar condiciones
    respuestas_previas = {
        str(r.pregunta_id): r.valor
        for r in sesion.respuestas.all()
    }

    form = DynamicPhaseForm(
        fase=fase,
        respuestas_previas=respuestas_previas,
        data=request.POST,
    )

    is_htmx = request.headers.get('HX-Request') == 'true'

    if form.is_valid():
        # Guardar respuestas de esta fase
        for field_name, value in form.cleaned_data.items():
            if field_name.startswith('pregunta_'):
                pregunta_id = int(field_name.split('_')[1])
                # Si es lista (checkbox), convertir a string separado por comas
                if isinstance(value, list):
                    value = ', '.join(value)
                RespuestaFormulario.objects.update_or_create(
                    sesion=sesion,
                    pregunta_id=pregunta_id,
                    defaults={'valor': str(value)},
                )

        # ¿Es la última fase?
        es_ultima = sesion.fase_actual >= total_fases

        if es_ultima:
            # Completar sesión — crear Lead si hay email
            _completar_sesion(request, sesion)
            context = {'sesion': sesion, 'formulario': formulario}
            if is_htmx:
                return render(request, 'components/formulario_completado.html', context)
            return render(request, 'landing/formulario_completado.html', context)

        # Avanzar a la siguiente fase
        sesion.fase_actual += 1
        sesion.save(update_fields=['fase_actual', 'actualizado_en'])

        siguiente_fase = fases[sesion.fase_actual - 1]
        # Actualizar respuestas previas con las recién guardadas
        respuestas_previas.update({
            field_name.replace('pregunta_', ''): str(v)
            for field_name, v in form.cleaned_data.items()
            if field_name.startswith('pregunta_')
        })

        next_form = DynamicPhaseForm(
            fase=siguiente_fase,
            respuestas_previas={
                str(r.pregunta_id): r.valor
                for r in sesion.respuestas.all()
            },
        )

        context = {
            'formulario': formulario,
            'fase': siguiente_fase,
            'fases': fases,
            'form': next_form,
            'sesion': sesion,
            'num_fase_actual': sesion.fase_actual,
            'total_fases': total_fases,
            'es_ultima_fase': sesion.fase_actual >= total_fases,
        }

        if is_htmx:
            return render(request, 'components/formulario_fase.html', context)
        return render(request, 'landing/formulario_dinamico.html', context)

    # Formulario inválido — volver a mostrar con errores
    context = {
        'formulario': formulario,
        'fase': fase,
        'fases': fases,
        'form': form,
        'sesion': sesion,
        'num_fase_actual': sesion.fase_actual,
        'total_fases': total_fases,
        'es_ultima_fase': sesion.fase_actual >= total_fases,
    }

    if is_htmx:
        return render(request, 'components/formulario_fase.html', context, status=422)
    return render(request, 'landing/formulario_dinamico.html', context, status=422)


# ──────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────

def _get_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        return ip.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _completar_sesion(request, sesion: SesionFormulario):
    """Marca la sesión como completada, crea Lead si hay email, envía email."""
    sesion.completado = True

    # Buscar campo email entre las respuestas para crear un Lead
    respuesta_email = sesion.respuestas.filter(
        pregunta__tipo_campo='email'
    ).first()
    respuesta_nombre = sesion.respuestas.filter(
        pregunta__tipo_campo='text',
        pregunta__orden=0,
    ).first()

    if respuesta_email:
        nombre = respuesta_nombre.valor if respuesta_nombre else 'Sin nombre'
        lead, _ = Lead.objects.get_or_create(
            email=respuesta_email.valor,
            defaults={
                'nombre': nombre,
                'mensaje': f'Via formulario dinámico: {sesion.formulario.nombre}',
            }
        )
        sesion.lead = lead

    sesion.save(update_fields=['completado', 'lead', 'actualizado_en'])

    # Enviar email de notificación
    _enviar_email_formulario(sesion)


def _enviar_email_formulario(sesion: SesionFormulario):
    """Envía email con todas las respuestas del formulario agrupadas por fase."""
    if not settings.RESEND_API_KEY:
        return

    resend.api_key = settings.RESEND_API_KEY

    # Construir HTML con respuestas agrupadas por fase
    fases_html = ""
    for grupo in sesion.get_respuestas_agrupadas():
        fase = grupo['fase']
        respuestas = grupo['respuestas']
        filas = ""
        for r in respuestas:
            filas += f"""
            <tr>
                <td style="padding:8px 12px;font-weight:600;color:#374151;background:#F9FAFB;width:45%;border-bottom:1px solid #E5E7EB;">{r.pregunta.etiqueta}</td>
                <td style="padding:8px 12px;color:#4B5563;border-bottom:1px solid #E5E7EB;">{r.valor or '—'}</td>
            </tr>"""

        icono = fase.icono or '📋'
        fases_html += f"""
        <div style="margin-bottom:24px;">
            <h3 style="color:#1E40AF;font-size:15px;margin:0 0 8px 0;padding:10px 14px;background:#EFF6FF;border-radius:8px;">
                {icono} {fase.titulo}
            </h3>
            <table style="width:100%;border-collapse:collapse;border:1px solid #E5E7EB;border-radius:8px;overflow:hidden;">
                {filas}
            </table>
        </div>"""

    nombre_display = sesion.lead.nombre if sesion.lead else 'Anónimo'
    email_display = sesion.lead.email if sesion.lead else '—'

    html_content = f"""
    <div style="font-family:sans-serif;max-width:640px;margin:0 auto;">
        <div style="background:linear-gradient(135deg,#0066FF,#22C55E);padding:24px;border-radius:12px 12px 0 0;">
            <h1 style="color:white;margin:0;font-size:20px;">
                📋 Nueva Respuesta — {sesion.formulario.nombre}
            </h1>
            <p style="color:rgba(255,255,255,0.8);margin:8px 0 0;font-size:14px;">
                Formulario completado por {nombre_display} ({email_display})
            </p>
        </div>
        <div style="background:#F9FAFB;padding:24px;border-radius:0 0 12px 12px;border:1px solid #E5E7EB;border-top:0;">
            {fases_html}
            <div style="margin-top:16px;padding:14px;background:white;border-radius:8px;border-left:4px solid #0066FF;">
                <a href="{settings.SITE_URL}/admin/landing/sesionformulario/{sesion.pk}/change/"
                   style="color:#0066FF;text-decoration:none;font-weight:bold;font-size:14px;">
                    → Ver respuesta completa en el Admin Panel
                </a>
            </div>
        </div>
    </div>
    """

    nombre_lead = sesion.lead.nombre if sesion.lead else 'Anónimo'
    
    # Generar PDF para adjuntar
    try:
        import base64
        pdf_buffer = generar_pdf_sesion(sesion)
        pdf_content = pdf_buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    except Exception as e:
        print(f"Error generando PDF: {e}")
        pdf_content = None

    try:
        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [settings.CONTACT_EMAIL],
            "subject": f"[SmartSolutions] Formulario completado: {sesion.formulario.nombre} — {nombre_lead}",
            "html": html_content,
        }
        
        if pdf_content:
            params["attachments"] = [
                {
                    "filename": f"Reporte_{sesion.formulario.slug}_{sesion.pk}.pdf",
                    "content": pdf_base64
                }
            ]
            
        resend.Emails.send(params)
    except Exception as e:
        print(f"Error enviando email formulario: {e}")


def descargar_pdf_sesion(request, sesion_id):
    """Permite descargar el reporte PDF de una sesión específica."""
    sesion = get_object_or_404(SesionFormulario, pk=sesion_id)
    
    # Seguridad básica: solo si el usuario tiene el ID en su sesión o es staff
    if not request.user.is_staff and request.session.get(f'formulario_sesion_{sesion.formulario_id}') != sesion.pk:
         return HttpResponse("No tienes permiso para ver este reporte.", status=403)

    try:
        pdf_buffer = generar_pdf_sesion(sesion)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Reporte_SmartSolutions_{sesion.pk}.pdf"'
        return response
    except Exception as e:
        return HttpResponse(f"Error generando el PDF: {e}", status=500)


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
        print(f"Error enviando email: {e}")
