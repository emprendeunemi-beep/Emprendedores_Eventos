from django.urls import path

from .views import RegistroEmprendedorView, RegistroExitosoView

app_name = 'emprendedores'

urlpatterns = [
    path('registro/', RegistroEmprendedorView.as_view(), name='registro'),
    path('registro/exitoso/', RegistroExitosoView.as_view(), name='registro_exitoso'),
]