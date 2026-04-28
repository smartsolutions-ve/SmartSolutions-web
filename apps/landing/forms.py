from django import forms
from .models import Lead, PreguntaFormulario


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


# ──────────────────────────────────────────────────────────
# FORMULARIO DINÁMICO
# ──────────────────────────────────────────────────────────

# Clases CSS compartidas para mantener consistencia visual
_FIELD_CLASS = (
    'w-full px-5 py-3.5 bg-white border border-slate-200 rounded-xl '
    'focus:outline-none focus:ring-2 focus:ring-brand-blue-400 focus:border-brand-blue-400 '
    'transition-all duration-200 text-slate-900 placeholder-slate-400'
)
_SELECT_CLASS = _FIELD_CLASS
_TEXTAREA_CLASS = (
    'w-full px-5 py-3.5 bg-white border border-slate-200 rounded-xl '
    'focus:outline-none focus:ring-2 focus:ring-brand-blue-400 focus:border-brand-blue-400 '
    'transition-all duration-200 text-slate-900 placeholder-slate-400 resize-none'
)


class DynamicPhaseForm(forms.Form):
    """
    Formulario generado dinámicamente a partir de las PreguntaFormulario
    de una FaseFormulario específica.

    Evalúa condiciones: si una pregunta tiene condicion_pregunta,
    solo se incluye si la respuesta previa coincide con condicion_valor.
    """

    def __init__(self, fase, respuestas_previas=None, *args, **kwargs):
        """
        fase: instancia de FaseFormulario
        respuestas_previas: dict {pregunta_id: valor_str} con respuestas de fases anteriores
        """
        super().__init__(*args, **kwargs)
        self.fase = fase
        respuestas_previas = respuestas_previas or {}

        for pregunta in fase.preguntas.order_by('orden'):
            # Evaluar condición de visibilidad
            if pregunta.condicion_pregunta_id:
                valor_previo = respuestas_previas.get(str(pregunta.condicion_pregunta_id), '')
                if valor_previo != pregunta.condicion_valor:
                    continue  # Omitir campo condicional no cumplido

            field_name = f'pregunta_{pregunta.pk}'
            field = self._build_field(pregunta)
            if field:
                self.fields[field_name] = field

    def _build_field(self, pregunta: PreguntaFormulario):
        """Construye el Field de Django apropiado según el tipo de la pregunta."""
        tipo = pregunta.tipo_campo
        label = pregunta.etiqueta
        requerido = pregunta.requerido
        placeholder = pregunta.placeholder
        help_text = pregunta.texto_ayuda
        opciones = pregunta.get_opciones_list()

        base_kwargs = dict(
            label=label,
            required=requerido,
            help_text=help_text,
        )

        if tipo == 'text':
            field = forms.CharField(
                **base_kwargs,
                widget=forms.TextInput(attrs={
                    'class': _FIELD_CLASS,
                    'placeholder': placeholder,
                })
            )

        elif tipo == 'email':
            field = forms.EmailField(
                **base_kwargs,
                widget=forms.EmailInput(attrs={
                    'class': _FIELD_CLASS,
                    'placeholder': placeholder,
                    'autocomplete': 'email',
                })
            )

        elif tipo == 'tel':
            field = forms.CharField(
                **base_kwargs,
                widget=forms.TextInput(attrs={
                    'class': _FIELD_CLASS,
                    'placeholder': placeholder,
                    'type': 'tel',
                    'autocomplete': 'tel',
                })
            )

        elif tipo == 'number':
            field = forms.IntegerField(
                **base_kwargs,
                widget=forms.NumberInput(attrs={
                    'class': _FIELD_CLASS,
                    'placeholder': placeholder,
                })
            )

        elif tipo == 'textarea':
            field = forms.CharField(
                **base_kwargs,
                widget=forms.Textarea(attrs={
                    'class': _TEXTAREA_CLASS,
                    'placeholder': placeholder,
                    'rows': 4,
                })
            )

        elif tipo == 'select':
            choices = [('', '— Selecciona una opción —')] + opciones
            field = forms.ChoiceField(
                **base_kwargs,
                choices=choices,
                widget=forms.Select(attrs={'class': _SELECT_CLASS})
            )

        elif tipo == 'radio':
            field = forms.ChoiceField(
                **base_kwargs,
                choices=opciones,
                widget=forms.RadioSelect(attrs={'class': 'dynamic-radio'})
            )

        elif tipo == 'checkbox':
            field = forms.MultipleChoiceField(
                **base_kwargs,
                choices=opciones,
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'dynamic-checkbox'}),
            )

        elif tipo == 'date':
            field = forms.DateField(
                **base_kwargs,
                widget=forms.DateInput(attrs={
                    'class': _FIELD_CLASS,
                    'type': 'date',
                })
            )

        else:
            return None

        # Guardar referencia a la pregunta en el field para uso en templates
        field.pregunta = pregunta
        return field

    def get_fields_con_pregunta(self):
        """Yield (field_name, bound_field, pregunta) para el template."""
        for name, field in self.fields.items():
            bound = self[name]
            pregunta = getattr(field, 'pregunta', None)
            yield name, bound, pregunta
