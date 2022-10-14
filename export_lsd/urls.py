from django.urls import path

from export_lsd.export_db import exportaDB, exportaDB_f931
from export_lsd.export_basic_txt import export_txt
from export_lsd.views import (advanced_export, HomeView,
                              ConfigEBCreateView, ConfigEBDeleteView, ConfigEBListView,
                              ConfigEBUpdateView,
                              EmpleadoCreateView, EmpleadoDeleteView, EmpleadoListView,
                              EmpleadoUpdateView, EmpresaCreateView, EmpresaDeleteView,
                              EmpresaListView, EmpresaUpdateView)

app_name = 'export_lsd'

urlpatterns = [
    # Panel
    path('', HomeView.as_view(), name='home'),

    # Empresas
    path('empresa/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresa/add/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresa/update/<int:pk>/', EmpresaUpdateView.as_view(), name='empresa_update'),
    path('empresa/delete/<int:pk>/', EmpresaDeleteView.as_view(), name='empresa_delete'),

    # Empleados
    path('empleado/', EmpleadoListView.as_view(), name='empleado_list'),
    path('empleado/add/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleado/update/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleado/delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),

    # Exportación  -------------------------------------------------------------
    # Configuración Exportación Básica
    path('config-eb/', ConfigEBListView.as_view(), name='config_eb_list'),
    path('config-eb/add/', ConfigEBCreateView.as_view(), name='config_eb_create'),
    path('config-eb/update/<int:pk>/', ConfigEBUpdateView.as_view(), name='config_eb_update'),
    path('config-eb/delete/<int:pk>/', ConfigEBDeleteView.as_view(), name='config_eb_delete'),

    # Accesos
    path('advanced/', advanced_export, name='advanced'),
    path('exportadb/', exportaDB),
    path('exportadb-f931/', exportaDB_f931),
    path('export_test/', export_txt),
]
