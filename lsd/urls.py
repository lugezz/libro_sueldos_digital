from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('export-lsd/', include('export_lsd.urls', namespace='export_lsd')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'export_lsd.views.error_404'
