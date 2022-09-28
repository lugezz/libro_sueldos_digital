from django.shortcuts import render


def home_view(request):
    return render(request, 'export_lsd/home.html', {})
