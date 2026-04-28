from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.landing, name='index'),
    path('contacto/', views.contacto_submit, name='contacto_submit'),

    # Formularios dinámicos
    path('formulario/', views.formulario_inicio, name='formulario_inicio'),
    path('formulario/<slug:slug>/', views.formulario_inicio, name='formulario_por_slug'),
    path('formulario/fase/<int:sesion_id>/', views.formulario_fase, name='formulario_fase'),
    path('formulario/pdf/<int:sesion_id>/', views.descargar_pdf_sesion, name='descargar_pdf_sesion'),
]
