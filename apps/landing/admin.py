from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import (
    Servicio, Testimonio, CasoDeExito, Lead,
    Formulario, FaseFormulario, PreguntaFormulario,
    SesionFormulario, RespuestaFormulario,
)


# ──────────────────────────────────────────────────────────
# CONTENIDO EXISTENTE
# ──────────────────────────────────────────────────────────

@admin.register(Servicio)
class ServicioAdmin(ModelAdmin):
    list_display = ('titulo', 'icono', 'beneficio_clave', 'orden', 'activo')
    list_editable = ('orden', 'activo')
    list_filter = ('activo',)
    search_fields = ('titulo', 'descripcion_corta')
    fieldsets = (
        ("Contenido", {
            "fields": ("titulo", "icono", "descripcion_corta", "descripcion_larga", "beneficio_clave"),
        }),
        ("Configuración", {
            "fields": ("orden", "activo"),
        }),
    )


@admin.register(Testimonio)
class TestimonioAdmin(ModelAdmin):
    list_display = ('nombre_cliente', 'empresa', 'sector', 'resultado_clave', 'destacado', 'activo')
    list_editable = ('destacado', 'activo')
    list_filter = ('activo', 'destacado')
    search_fields = ('nombre_cliente', 'empresa', 'texto')
    fieldsets = (
        ("Cliente", {
            "fields": ("nombre_cliente", "cargo", "empresa", "sector", "foto"),
        }),
        ("Testimonio", {
            "fields": ("texto", "resultado_clave"),
        }),
        ("Configuración", {
            "fields": ("orden", "destacado", "activo"),
        }),
    )


@admin.register(CasoDeExito)
class CasoDeExitoAdmin(ModelAdmin):
    list_display = ('titulo', 'empresa', 'sector', 'activo')
    list_editable = ('activo',)
    list_filter = ('activo', 'sector')
    search_fields = ('titulo', 'empresa', 'descripcion')
    fieldsets = (
        ("Información del Caso", {
            "fields": ("titulo", "empresa", "sector", "descripcion", "imagen"),
        }),
        ("Métricas de Impacto", {
            "fields": (
                ("metrica_1_valor", "metrica_1_label"),
                ("metrica_2_valor", "metrica_2_label"),
                ("metrica_3_valor", "metrica_3_label"),
            ),
        }),
        ("Configuración", {
            "fields": ("orden", "activo"),
        }),
    )


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = (
        'nombre', 'email', 'empresa',
        'servicio_interes_display', 'estado_badge',
        'creado_en'
    )
    list_filter = ('estado', 'servicio_interes', 'creado_en')
    search_fields = ('nombre', 'email', 'empresa', 'mensaje')
    readonly_fields = ('creado_en', 'actualizado_en', 'ip_origen')
    date_hierarchy = 'creado_en'

    fieldsets = (
        ("📋 Datos del Contacto", {
            "fields": ("nombre", "email", "telefono", "empresa", "servicio_interes"),
        }),
        ("💬 Mensaje", {
            "fields": ("mensaje",),
        }),
        ("🎯 Gestión Interna", {
            "fields": ("estado", "notas_internas"),
        }),
        ("📅 Metadata", {
            "fields": ("creado_en", "actualizado_en", "ip_origen"),
            "classes": ["collapse"],
        }),
    )

    def estado_badge(self, obj):
        colores = {
            'nuevo': '#0066FF',
            'contactado': '#22C55E',
            'en_proceso': '#F59E0B',
            'cerrado': '#6B7280',
            'descartado': '#EF4444',
        }
        color = colores.get(obj.estado, '#6B7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;border-radius:999px;font-size:12px">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"

    def servicio_interes_display(self, obj):
        return obj.get_servicio_interes_display()
    servicio_interes_display.short_description = "Servicio"

    def has_add_permission(self, request):
        return False


# ──────────────────────────────────────────────────────────
# SISTEMA DE FORMULARIOS DINÁMICOS
# ──────────────────────────────────────────────────────────

class PreguntaFormularioInline(StackedInline):
    model = PreguntaFormulario
    extra = 1
    fields = (
        ('etiqueta', 'tipo_campo', 'ancho'),
        ('placeholder', 'texto_ayuda'),
        ('requerido', 'orden'),
        'opciones',
        ('condicion_pregunta', 'condicion_valor'),
    )
    verbose_name = "Pregunta"
    verbose_name_plural = "Preguntas de esta Fase"


class FaseFormularioInline(StackedInline):
    model = FaseFormulario
    extra = 1
    fields = (('titulo', 'icono', 'orden'), 'descripcion')
    show_change_link = True
    verbose_name = "Fase"
    verbose_name_plural = "Fases del Formulario"


@admin.register(Formulario)
class FormularioAdmin(ModelAdmin):
    list_display = ('nombre', 'slug', 'es_principal', 'activo', 'num_fases', 'creado_en')
    list_editable = ('es_principal', 'activo')
    list_filter = ('activo', 'es_principal')
    search_fields = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [FaseFormularioInline]

    fieldsets = (
        ("📝 Información del Formulario", {
            "fields": ("nombre", "slug", "descripcion"),
        }),
        ("⚙️ Configuración", {
            "fields": ("activo", "es_principal"),
            "description": "Si 'Es Principal' está activo, este formulario reemplaza la sección de contacto en la landing page.",
        }),
    )

    def num_fases(self, obj):
        n = obj.fases.count()
        return format_html(
            '<span style="background:#EFF6FF;color:#1D4ED8;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:600">{} {}</span>',
            n, "fase" if n == 1 else "fases"
        )
    num_fases.short_description = "Fases"


@admin.register(FaseFormulario)
class FaseFormularioAdmin(ModelAdmin):
    list_display = ('titulo', 'formulario', 'orden', 'num_preguntas')
    list_filter = ('formulario',)
    search_fields = ('titulo', 'formulario__nombre')
    ordering = ('formulario', 'orden')
    inlines = [PreguntaFormularioInline]

    fieldsets = (
        ("Fase", {
            "fields": (('titulo', 'icono', 'orden'), 'descripcion', 'formulario'),
        }),
    )

    def num_preguntas(self, obj):
        n = obj.preguntas.count()
        return format_html(
            '<span style="background:#F0FDF4;color:#166534;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:600">{} {}</span>',
            n, "pregunta" if n == 1 else "preguntas"
        )
    num_preguntas.short_description = "Preguntas"


class RespuestaFormularioInline(TabularInline):
    model = RespuestaFormulario
    extra = 0
    readonly_fields = ('pregunta_fase', 'pregunta', 'valor')
    fields = ('pregunta_fase', 'pregunta', 'valor')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def pregunta_fase(self, obj):
        return obj.pregunta.fase.titulo
    pregunta_fase.short_description = "Fase"


@admin.register(SesionFormulario)
class SesionFormularioAdmin(ModelAdmin):
    list_display = (
        'formulario', 'nombre_lead', 'email_lead',
        'estado_badge', 'fase_actual', 'creado_en'
    )
    list_filter = ('formulario', 'completado', 'creado_en')
    search_fields = ('lead__nombre', 'lead__email')
    readonly_fields = (
        'formulario', 'lead', 'fase_actual',
        'completado', 'ip_origen', 'creado_en', 'actualizado_en'
    )
    date_hierarchy = 'creado_en'
    inlines = [RespuestaFormularioInline]

    fieldsets = (
        ("📋 Sesión", {
            "fields": ("formulario", "lead", "fase_actual", "completado"),
        }),
        ("📅 Metadata", {
            "fields": ("ip_origen", "creado_en", "actualizado_en"),
            "classes": ["collapse"],
        }),
    )

    def nombre_lead(self, obj):
        return obj.lead.nombre if obj.lead else "—"
    nombre_lead.short_description = "Nombre"

    def email_lead(self, obj):
        return obj.lead.email if obj.lead else "—"
    email_lead.short_description = "Email"

    def estado_badge(self, obj):
        if obj.completado:
            return format_html(
                '<span style="background:#22C55E;color:white;padding:2px 10px;border-radius:999px;font-size:12px">✅ Completada</span>'
            )
        return format_html(
            '<span style="background:#F59E0B;color:white;padding:2px 10px;border-radius:999px;font-size:12px">⏳ En Proceso</span>'
        )
    estado_badge.short_description = "Estado"

    def has_add_permission(self, request):
        return False
