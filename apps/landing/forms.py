from django import forms
from .models import Lead


class ContactoForm(forms.ModelForm):
    """
    Formulario de contacto principal de la landing.
    Crea un Lead en la BD y envía email de notificación.
    """

    class Meta:
        model = Lead
        fields = ['nombre', 'email', 'telefono', 'empresa', 'servicio_interes', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Tu nombre completo',
                'class': 'w-full px-6 py-4 bg-white border border-slate-200 rounded-2xl focus:outline-none focus:border-smart-blue transition-colors text-slate-900',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'tu@empresa.com',
                'class': 'w-full px-6 py-4 bg-white border border-slate-200 rounded-2xl focus:outline-none focus:border-smart-blue transition-colors text-slate-900',
                'autocomplete': 'email',
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': '+58 412 0000000',
                'class': 'w-full px-6 py-4 bg-white border border-slate-200 rounded-2xl focus:outline-none focus:border-smart-blue transition-colors text-slate-900',
                'autocomplete': 'tel',
            }),
            'empresa': forms.TextInput(attrs={
                'placeholder': 'Nombre de tu empresa',
                'class': 'w-full px-6 py-4 bg-white border border-slate-200 rounded-2xl focus:outline-none focus:border-smart-blue transition-colors text-slate-900',
            }),
            'servicio_interes': forms.Select(attrs={
                'class': 'w-full px-6 py-4 bg-white border border-slate-200 rounded-2xl focus:outline-none focus:border-smart-blue transition-colors text-slate-900',
            }),
            'mensaje': forms.Textarea(attrs={
                'placeholder': 'Cuéntanos sobre tu negocio y qué problema quieres resolver...',
                'class': 'w-full px-6 py-4 bg-white border border-slate-200 rounded-2xl focus:outline-none focus:border-smart-blue transition-colors text-slate-900',
                'rows': 4,
            }),
        }
        labels = {
            'nombre': 'Nombre completo *',
            'email': 'Correo electrónico *',
            'telefono': 'Teléfono / WhatsApp',
            'empresa': 'Empresa',
            'servicio_interes': '¿En qué servicio estás interesado?',
            'mensaje': 'Mensaje *',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['email'].required = True
        self.fields['mensaje'].required = True
        self.fields['telefono'].required = False
        self.fields['empresa'].required = False
