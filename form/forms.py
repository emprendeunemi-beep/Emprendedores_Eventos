from django import forms

from .models import (
    RegistroEmprendedor,
    CapacitacionChoices,
    SexoChoices,
    VinculacionChoices,
    CategoriaEmprendimientoChoices,
    TiempoFuncionamientoChoices,
    NumeroColaboradoresChoices,
    PermisosChoices,
)


class RegistroEmprendedorForm(forms.ModelForm):

    # Sobrescribimos capacitacion_intereses para usar MultipleChoiceField con checkboxes
    capacitacion_intereses = forms.MultipleChoiceField(
        choices=CapacitacionChoices.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='¿En cuáles temas le gustaría recibir capacitación?',
    )

    # tiene_ruc como select explícito (BooleanField por defecto usa checkbox)
    tiene_ruc = forms.ChoiceField(
        choices=[('', '---------'), ('True', 'Sí'), ('False', 'No')],
        label='¿Cuenta con RUC o RIMPE?',
    )

    # participo_anteriormente igual
    participo_anteriormente = forms.ChoiceField(
        choices=[('', '---------'), ('True', 'Sí'), ('False', 'No')],
        label='¿Ha participado anteriormente en actividades de la Gestión de Emprendimiento UNEMI?',
        required=False,
    )

    class Meta:
        model = RegistroEmprendedor
        fields = [
            # Sección 1
            'cedula',
            'nombres_apellidos',
            'edad',
            'sexo',
            'whatsapp',
            # Sección 2
            'vinculacion',
            'correo_institucional',
            'correo_personal',
            'carrera_actual',
            'semestre_actual',
            'carrera_graduado',
            # Sección 3
            'provincia',
            'canton',
            # Sección 4
            'nombre_emprendimiento',
            'descripcion_productos',
            'categoria',
            'categoria_otro',
            'tiempo_funcionamiento',
            'numero_colaboradores',
            'direccion',
            'redes_sociales',
            # Sección 5
            'tiene_ruc',
            'numero_ruc',
            'archivo_ruc',
            'permisos_funcionamiento',
            'archivo_permiso',
            # Sección 6
            'capacitacion_intereses',
            'capacitacion_otro',
            # Sección 7
            'participo_anteriormente',
            'comentarios',
        ]
        widgets = {
            'cedula':               forms.TextInput(attrs={'placeholder': 'Ej: 0912345678'}),
            'nombres_apellidos':    forms.TextInput(attrs={'placeholder': 'Nombres y apellidos completos'}),
            'edad':                 forms.NumberInput(attrs={'min': 1, 'max': 120}),
            'sexo':                 forms.Select(choices=[('', '---------')] + SexoChoices.choices),
            'whatsapp':             forms.TextInput(attrs={'placeholder': 'Ej: +593 99 999 9999'}),
            'vinculacion':          forms.Select(choices=[('', '---------')] + VinculacionChoices.choices),
            'correo_institucional': forms.EmailInput(attrs={'placeholder': 'usuario@unemi.edu.ec'}),
            'correo_personal':      forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'carrera_actual':       forms.TextInput(attrs={'placeholder': 'Nombre de la carrera'}),
            'semestre_actual':      forms.TextInput(attrs={'placeholder': 'Ej: 5to semestre'}),
            'carrera_graduado':     forms.TextInput(attrs={'placeholder': 'Carrera de la que se graduó'}),
            'provincia':            forms.TextInput(attrs={'placeholder': 'Provincia'}),
            'canton':               forms.TextInput(attrs={'placeholder': 'Cantón o ciudad'}),
            'nombre_emprendimiento': forms.TextInput(attrs={'placeholder': 'Nombre del negocio'}),
            'descripcion_productos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describa brevemente sus productos o servicios'}),
            'categoria':            forms.Select(choices=[('', '---------')] + CategoriaEmprendimientoChoices.choices),
            'categoria_otro':       forms.TextInput(attrs={'placeholder': 'Especifique la categoría'}),
            'tiempo_funcionamiento': forms.Select(choices=[('', '---------')] + TiempoFuncionamientoChoices.choices),
            'numero_colaboradores': forms.Select(choices=[('', '---------')] + NumeroColaboradoresChoices.choices),
            'direccion':            forms.TextInput(attrs={'placeholder': 'Dirección del emprendimiento'}),
            'redes_sociales':       forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ej: Instagram: @mi_negocio, Facebook: /minegocio'}),
            'numero_ruc':           forms.TextInput(attrs={'placeholder': 'Número de RUC o RIMPE'}),
            'permisos_funcionamiento': forms.Select(choices=[('', '---------')] + PermisosChoices.choices),
            'capacitacion_otro':    forms.TextInput(attrs={'placeholder': 'Detalle el tema de interés'}),
            'comentarios':          forms.Textarea(attrs={'rows': 4, 'placeholder': 'Comentarios, sugerencias o expectativas…'}),
        }

    # ── Validaciones condicionales según vinculación ─────────────────────────

    def clean(self):
        cleaned = super().clean()
        vinculacion = cleaned.get('vinculacion')

        if vinculacion == VinculacionChoices.ESTUDIANTE:
            for campo in ('correo_institucional', 'correo_personal', 'carrera_actual', 'semestre_actual'):
                if not cleaned.get(campo):
                    self.add_error(campo, 'Este campo es obligatorio para estudiantes.')

        elif vinculacion == VinculacionChoices.GRADUADO:
            for campo in ('correo_personal', 'carrera_graduado'):
                if not cleaned.get(campo):
                    self.add_error(campo, 'Este campo es obligatorio para graduados.')

        elif vinculacion in (VinculacionChoices.DOCENTE, VinculacionChoices.ADMINISTRATIVO):
            if not cleaned.get('correo_institucional'):
                self.add_error('correo_institucional', 'Este campo es obligatorio para docentes y personal administrativo.')

        elif vinculacion in (VinculacionChoices.RETIRADO, VinculacionChoices.EXTERNO, VinculacionChoices.OTRO):
            if not cleaned.get('correo_personal'):
                self.add_error('correo_personal', 'Este campo es obligatorio.')

        # RUC condicional
        tiene_ruc = cleaned.get('tiene_ruc')
        if tiene_ruc == 'True' and not cleaned.get('numero_ruc'):
            self.add_error('numero_ruc', 'Ingrese el número de RUC o RIMPE.')

        # Capacitación "Otro" condicional
        intereses = cleaned.get('capacitacion_intereses', [])
        if 'otro' in intereses and not cleaned.get('capacitacion_otro'):
            self.add_error('capacitacion_otro', 'Por favor detalle el tema de capacitación.')

        return cleaned

    # ── Conversión de campos booleanos desde string ──────────────────────────

    def clean_tiene_ruc(self):
        val = self.cleaned_data.get('tiene_ruc')
        if val == 'True':
            return True
        if val == 'False':
            return False
        raise forms.ValidationError('Seleccione una opción.')

    def clean_participo_anteriormente(self):
        val = self.cleaned_data.get('participo_anteriormente')
        if val == 'True':
            return True
        if val == 'False':
            return False
        return None  # campo opcional
