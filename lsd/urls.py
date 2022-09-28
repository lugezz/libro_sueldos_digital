from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('export_lsd.urls', namespace='export_lsd')),
]
