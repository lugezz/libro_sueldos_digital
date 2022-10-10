from django.shortcuts import render


def home_view(request):
    return render(request, 'export_lsd/home.html', {})


def advanced_export(request):

    context = {
        'title': 'Exportación Avanzada',
    }

    return render(request, 'export_lsd/advanced.html', context)
