from django.urls import path

from .views import EmprendedoresListView
app_name = 'portal'

urlpatterns = [
    path('emprendedores/', EmprendedoresListView.as_view(), name='listado'),
]