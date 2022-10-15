import datetime
from tablib import Dataset
from tablib.exceptions import UnsupportedFormat

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from export_lsd.models import BasicExportConfig, Empleado, Empresa, Registro
from export_lsd.forms import ConfigEBForm, EmpresaForm, EmpleadoForm
from export_lsd.resources import EmpleadoResource


# ------------- DASHBOARD ------------------------------------------------
class HomeView(TemplateView):
    template_name = 'export_lsd/home.html'

    def get_context_data(self, **kwargs):
        query_historia = Registro.objects.filter(empresa__user=self.request.user)
        today = datetime.date.today()
        last_month = today.replace(day=1) - datetime.timedelta(days=1)
        last_month_str = last_month.strftime("%Y-%m")

        context = super().get_context_data(**kwargs)
        context['query'] = query_historia
        context['this_month'] = last_month_str
        # TODO: Resumen, cantidad de liquidaciones, empleados y total remuneración
        context['listado'] = last_month_str

        return context


# ------------- EMPRESAS ------------------------------------------------
class EmpresaListView(LoginRequiredMixin, ListView):
    model = Empresa
    template_name = 'export_lsd/empresa/list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Empresa.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Empresas'
        context['create_url'] = reverse_lazy('export_lsd:empresa_create')
        context['list_url'] = reverse_lazy('export_lsd:empresa_list')
        context['entity'] = 'Empresas'
        return context


class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'export_lsd/empresa/create.html'
    success_url = reverse_lazy('export_lsd:empresa_list')
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()  # Es lo mismo que escribir form = EmpresaForm(request.POST)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Empresa'
        context['list_url'] = reverse_lazy('export_lsd:empresa_list')
        context['entity'] = 'Empresas'
        context['action'] = 'add'
        return context


class EmpresaUpdateView(LoginRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'export_lsd/empresa/create.html'
    success_url = reverse_lazy('export_lsd:empresa_list')
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()  # Es lo mismo que escribir form = EmpresaForm(request.POST)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'

        except Exception as e:
            data['error'] = e

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Empresa'
        context['list_url'] = reverse_lazy('export_lsd:empresa_list')
        context['entity'] = 'Empresas'
        context['action'] = 'edit'
        return context


class EmpresaDeleteView(LoginRequiredMixin, DeleteView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'export_lsd/empresa/delete.html'
    success_url = reverse_lazy('export_lsd:empresa_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = e

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Empresa'
        context['list_url'] = reverse_lazy('export_lsd:empresa_list')
        context['entity'] = 'Empresas'
        return context


# ------------- EMPLEADOS ------------------------------------------------
class EmpleadoListView(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'export_lsd/empleado/list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Empleado.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Empleados'
        context['create_url'] = reverse_lazy('export_lsd:empleado_create')
        context['list_url'] = reverse_lazy('export_lsd:empleado_list')
        context['entity'] = 'Empleados'
        return context


class EmpleadoCreateView(LoginRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'export_lsd/empleado/create.html'
    success_url = reverse_lazy('export_lsd:empleado_list')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Empleado'
        context['entity'] = 'Empleados'
        context['list_url'] = reverse_lazy('export_lsd:empleado_list')
        context['action'] = 'add'
        return context


class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'export_lsd/empleado/create.html'
    success_url = reverse_lazy('export_lsd:empleado_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Empleado'
        context['entity'] = 'Empleados'
        context['list_url'] = reverse_lazy('export_lsd:empleado_list')
        context['action'] = 'edit'
        return context


class EmpleadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Empleado
    template_name = 'export_lsd/empleado/delete.html'
    success_url = reverse_lazy('export_lsd:empleado_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Empleado'
        context['entity'] = 'Empleados'
        context['list_url'] = reverse_lazy('export_lsd:empleado_list')
        return context


# ------------- EXPORT ------------------------------------------------
def basic_export(request):
    context = {
        'error': '',
        'results': ''
    }

    if request.method == 'POST':
        persona_resource = EmpleadoResource()
        dataset = Dataset()
        print(dataset)
        nuevos_empleados = request.FILES['xlsfile']
        print(nuevos_empleados)
        try:
            imported_data = dataset.load(nuevos_empleados.read())
            print(imported_data)
        except UnsupportedFormat:
            context['error'] = "Formato de archivo incorrecto"
        except Exception as err:
            context['error'] = f"Unexpected {err=}, {type(err)=}"

        # Test the data import  #print(result.has_errors())
        result = persona_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            print(result)

    return render(request, 'export_lsd/export/basic.html', context)


def advanced_export(request):

    context = {
        'title': 'Exportación Avanzada',
    }

    return render(request, 'export_lsd/advanced.html', context)


# ------------- CONFIGURACIÓN EXPORTACIÓN BÁSICA ------------------------------------------------
class ConfigEBListView(LoginRequiredMixin, ListView):
    model = BasicExportConfig
    template_name = 'export_lsd/config-eb/list.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # TODO: Filtrar por usuarios en todos lados
                for i in BasicExportConfig.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configuraciones de Exportaciones Básicas'
        context['create_url'] = reverse_lazy('export_lsd:config_eb_create')
        context['list_url'] = reverse_lazy('export_lsd:config_eb_list')
        context['entity'] = 'ConfigEB'
        return context


class ConfigEBCreateView(LoginRequiredMixin, CreateView):
    model = BasicExportConfig
    form_class = ConfigEBForm
    template_name = 'export_lsd/config-eb/create.html'
    success_url = reverse_lazy('export_lsd:config_eb_list')
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Configuración'
        context['list_url'] = reverse_lazy('export_lsd:config_eb_list')
        context['entity'] = 'ConfigEB'
        context['action'] = 'add'
        return context


class ConfigEBUpdateView(LoginRequiredMixin, UpdateView):
    model = BasicExportConfig
    form_class = ConfigEBForm
    template_name = 'export_lsd/config-eb/create.html'
    success_url = reverse_lazy('export_lsd:config_eb_list')
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'

        except Exception as e:
            data['error'] = e

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Configuración'
        context['list_url'] = reverse_lazy('export_lsd:config_eb_list')
        context['entity'] = 'ConfigEB'
        context['action'] = 'edit'
        return context


class ConfigEBDeleteView(LoginRequiredMixin, DeleteView):
    model = BasicExportConfig
    form_class = ConfigEBForm
    template_name = 'export_lsd/config-eb/delete.html'
    success_url = reverse_lazy('export_lsd:config_eb_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = e

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Configuración'
        context['list_url'] = reverse_lazy('export_lsd:config_eb_list')
        context['entity'] = 'ConfigEB'
        return context
