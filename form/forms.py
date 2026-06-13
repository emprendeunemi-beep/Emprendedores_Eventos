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

    # Campos con validación condicional — required=False para que
    # el método clean() controle cuándo son obligatorios
    correo_institucional = forms.EmailField(
        required=False,
        label='Correo institucional UNEMI',
        widget=forms.EmailInput(attrs={'placeholder': 'usuario@unemi.edu.ec'}),
    )
    correo_personal = forms.EmailField(
        required=False,
        label='Correo electrónico personal',
        widget=forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
    )
    carrera_actual = forms.CharField(
        required=False,
        label='Carrera que cursa actualmente',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de la carrera'}),
    )
    semestre_actual = forms.CharField(
        required=False,
        label='Semestre actual',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 5to semestre'}),
    )
    carrera_graduado = forms.CharField(
        required=False,
        label='Carrera de graduación',
        widget=forms.TextInput(attrs={'placeholder': 'Carrera de la que se graduó'}),
    )

    # Selección múltiple con checkboxes
    capacitacion_intereses = forms.MultipleChoiceField(
        choices=CapacitacionChoices.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='¿En cuáles temas le gustaría recibir capacitación?',
    )

    # BooleanFields como select Sí/No
    tiene_ruc = forms.ChoiceField(
        choices=[('', '---------'), ('True', 'Sí'), ('False', 'No')],
        label='¿Cuenta con RUC o RIMPE?',
    )
    participo_anteriormente = forms.ChoiceField(
        choices=[('', '---------'), ('True', 'Sí'), ('False', 'No')],
        label='¿Ha participado anteriormente en actividades de la Gestión de Emprendimiento UNEMI?',
        required=False,
    )

    class Meta:
        model = RegistroEmprendedor
        fields = [
            'cedula', 'nombres_apellidos', 'edad', 'sexo', 'whatsapp',
            'vinculacion',
            'correo_institucional', 'correo_personal',
            'carrera_actual', 'semestre_actual', 'carrera_graduado',
            'provincia', 'canton',
            'nombre_emprendimiento', 'descripcion_productos',
            'categoria', 'categoria_otro',
            'tiempo_funcionamiento', 'numero_colaboradores',
            'direccion', 'redes_sociales',
            'tiene_ruc', 'numero_ruc', 'archivo_ruc',
            'permisos_funcionamiento', 'archivo_permiso',
            'capacitacion_intereses', 'capacitacion_otro',
            'participo_anteriormente', 'comentarios',
        ]
        widgets = {
            'cedula':                forms.TextInput(attrs={'placeholder': 'Ej: 0912345678'}),
            'nombres_apellidos':     forms.TextInput(attrs={'placeholder': 'Nombres y apellidos completos'}),
            'edad':                  forms.NumberInput(attrs={'min': 1, 'max': 120}),
            'sexo':                  forms.Select(choices=[('', '---------')] + SexoChoices.choices),
            'whatsapp':              forms.TextInput(attrs={'placeholder': 'Ej: +593 99 999 9999'}),
            'vinculacion':           forms.Select(choices=[('', '---------')] + VinculacionChoices.choices),
            # correo_institucional, correo_personal, carrera_actual,
            # semestre_actual y carrera_graduado se definen arriba como campos
            # explícitos con required=False, por eso no van aquí en widgets.
            'provincia':             forms.TextInput(attrs={'placeholder': 'Provincia'}),
            'canton':                forms.TextInput(attrs={'placeholder': 'Cantón o ciudad'}),
            'nombre_emprendimiento': forms.TextInput(attrs={'placeholder': 'Nombre del negocio'}),
            'descripcion_productos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describa brevemente sus productos o servicios'}),
            'categoria':             forms.Select(choices=[('', '---------')] + CategoriaEmprendimientoChoices.choices),
            'categoria_otro':        forms.TextInput(attrs={'placeholder': 'Especifique la categoría'}),
            'tiempo_funcionamiento': forms.Select(choices=[('', '---------')] + TiempoFuncionamientoChoices.choices),
            'numero_colaboradores':  forms.Select(choices=[('', '---------')] + NumeroColaboradoresChoices.choices),
            'direccion':             forms.TextInput(attrs={'placeholder': 'Dirección del emprendimiento'}),
            'redes_sociales':        forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ej: Instagram: @mi_negocio'}),
            'numero_ruc':            forms.TextInput(attrs={'placeholder': 'Número de RUC o RIMPE'}),
            'permisos_funcionamiento': forms.Select(choices=[('', '---------')] + PermisosChoices.choices),
            'capacitacion_otro':     forms.TextInput(attrs={'placeholder': 'Detalle el tema de interés'}),
            'comentarios':           forms.Textarea(attrs={'rows': 4, 'placeholder': 'Comentarios, sugerencias o expectativas…'}),
        }

    # ── Validación condicional según vinculación ─────────────────────────────
    def clean(self):
        cleaned = super().clean()
        vinculacion = cleaned.get('vinculacion')
        correo_personal = cleaned.get('correo_personal')

        if vinculacion == VinculacionChoices.ESTUDIANTE:
            if not cleaned.get('correo_institucional'):
                self.add_error('correo_institucional', 'Este campo es obligatorio para estudiantes.')
            if not correo_personal:
                self.add_error('correo_personal', 'Este campo es obligatorio para estudiantes.')
            if not cleaned.get('carrera_actual'):
                self.add_error('carrera_actual', 'Este campo es obligatorio para estudiantes.')
            if not cleaned.get('semestre_actual'):
                self.add_error('semestre_actual', 'Este campo es obligatorio para estudiantes.')

        elif vinculacion == VinculacionChoices.GRADUADO:
            if not correo_personal:
                self.add_error('correo_personal', 'Este campo es obligatorio para graduados.')
            if not cleaned.get('carrera_graduado'):
                self.add_error('carrera_graduado', 'Este campo es obligatorio para graduados.')

        elif vinculacion in (VinculacionChoices.DOCENTE, VinculacionChoices.ADMINISTRATIVO):
            if not cleaned.get('correo_institucional'):
                self.add_error('correo_institucional', 'Este campo es obligatorio para docentes y personal administrativo.')

        elif vinculacion in (VinculacionChoices.RETIRADO, VinculacionChoices.EXTERNO, VinculacionChoices.OTRO):
            if not correo_personal:
                self.add_error('correo_personal', 'Este campo es obligatorio.')

        # RUC condicional
        if cleaned.get('tiene_ruc') == 'True' and not cleaned.get('numero_ruc'):
            self.add_error('numero_ruc', 'Ingrese el número de RUC o RIMPE.')

        # Capacitación "Otro"
        if 'otro' in cleaned.get('capacitacion_intereses', []) and not cleaned.get('capacitacion_otro'):
            self.add_error('capacitacion_otro', 'Por favor detalle el tema de capacitación.')

        return cleaned

    # ── Conversión de booleanos ──────────────────────────────────────────────
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
        return None