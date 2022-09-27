from django.urls import path

from tables.export_db import exportaDB, exportaDB_f931
from tables.export_txt import export_txt
from tables.views import home_view

app_name = 'tables'

urlpatterns = [
    path('', home_view, name='home'),
    path('exportadb/', exportaDB),
    path('exportadb-f931/', exportaDB_f931),
    path('export_test/', export_txt),
]
