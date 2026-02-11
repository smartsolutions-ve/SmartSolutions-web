from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Servicio, Testimonio, CasoDeExito, Lead


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
        # Los leads solo se crean desde el formulario público
        return False
