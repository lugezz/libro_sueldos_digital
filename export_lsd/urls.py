from django.urls import path

from export_lsd.export_db import exportaDB, exportaDB_f931
from export_lsd.export_basic_txt import export_txt
from export_lsd.views import home_view, advanced_export

app_name = 'export_lsd'

urlpatterns = [
    path('', home_view, name='home'),
    path('advanced/', advanced_export, name='advanced'),

    path('exportadb/', exportaDB),
    path('exportadb-f931/', exportaDB_f931),
    path('export_test/', export_txt),
]
