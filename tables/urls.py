from django.urls import path

from tables.export_db import exportaDB
from tables.views import home_view

app_name = 'tables'

urlpatterns = [
    path('', home_view, name='home'),
    path('exportadb/', exportaDB),
]