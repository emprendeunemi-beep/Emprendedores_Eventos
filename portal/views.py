from django.views.generic import ListView
from django.db.models import Q
from form.models import RegistroEmprendedor


class EmprendedoresListView(ListView):
    model = RegistroEmprendedor
    template_name = 'emprendedores_list.html'
    context_object_name = 'emprendedores'
    paginate_by = 20

    def get_queryset(self):
        qs = RegistroEmprendedor.objects.all()

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(nombres_apellidos__icontains=q) |
                Q(cedula__icontains=q) |
                Q(nombre_emprendimiento__icontains=q)
            )

        categoria = self.request.GET.get('categoria', '').strip()
        if categoria:
            qs = qs.filter(categoria=categoria)

        vinculacion = self.request.GET.get('vinculacion', '').strip()
        if vinculacion:
            qs = qs.filter(vinculacion=vinculacion)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Conservar parámetros de búsqueda en la paginación
        params = self.request.GET.copy()
        params.pop('page', None)
        ctx['query_string'] = params.urlencode()

        # Opciones para los filtros
        from form.models import CategoriaEmprendimientoChoices, VinculacionChoices
        ctx['categorias'] = CategoriaEmprendimientoChoices.choices
        ctx['vinculaciones'] = VinculacionChoices.choices
        ctx['filtro_categoria'] = self.request.GET.get('categoria', '')
        ctx['filtro_vinculacion'] = self.request.GET.get('vinculacion', '')
        ctx['q'] = self.request.GET.get('q', '')
        return ctx