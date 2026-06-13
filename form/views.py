from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from .forms import RegistroEmprendedorForm
from .models import RegistroEmprendedor, VinculacionChoices


class RegistroEmprendedorView(View):
    template_name = 'registro.html'

    def get(self, request):
        form = RegistroEmprendedorForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistroEmprendedorForm(request.POST, request.FILES)
        if form.is_valid():
            registro = form.save(commit=False)

            # ── Lógica condicional según vinculación ─────────────────────────
            vinculacion = form.cleaned_data['vinculacion']

            if vinculacion == VinculacionChoices.ESTUDIANTE:
                # correo_institucional + correo_personal + carrera_actual + semestre_actual
                pass

            elif vinculacion == VinculacionChoices.GRADUADO:
                # correo_personal + carrera_graduado; limpiar campos de estudiante
                registro.correo_institucional = None
                registro.carrera_actual = None
                registro.semestre_actual = None

            elif vinculacion in (VinculacionChoices.DOCENTE, VinculacionChoices.ADMINISTRATIVO):
                # correo_institucional obligatorio; correo_personal opcional
                registro.carrera_actual = None
                registro.semestre_actual = None
                registro.carrera_graduado = None

            else:  # RETIRADO, EXTERNO, OTRO
                # solo correo_personal
                registro.correo_institucional = None
                registro.carrera_actual = None
                registro.semestre_actual = None
                registro.carrera_graduado = None

            # ── Intereses de capacitación (múltiple selección) ───────────────
            registro.capacitacion_intereses = form.cleaned_data.get('capacitacion_intereses', [])

            registro.save()

            messages.success(
                request,
                f'¡Registro exitoso! Bienvenido/a a la Red de Emprendedores UNEMI, {registro.nombres_apellidos}.',
            )
            return redirect('emprendedores:registro_exitoso')

        # Si el formulario tiene errores, reenviar con los datos ingresados
        return render(request, self.template_name, {'form': form})


class RegistroExitosoView(View):
    template_name = 'registro_exitoso.html'

    def get(self, request):
        return render(request, self.template_name)