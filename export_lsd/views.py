import datetime

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from export_lsd.models import BasicExportConfig, BulkCreateManager, Empleado, Empresa, Registro
from export_lsd.forms import ConfigEBForm, EmpresaForm, EmpleadoForm
from export_lsd.tools.export_basic_txt import export_txt
from export_lsd.tools.import_empleados import get_employees


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
        context['import_url'] = reverse_lazy('export_lsd:import_empleados')
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
@login_required
def basic_export(request):
    # Debe tener al menos una configuración básica
    basic_export_config_qs = BasicExportConfig.objects.filter(user=request.user)

    if not basic_export_config_qs:
        messages.error(request, "Debe crear al menos un modelo de configuración de Exportación Básica")
        return redirect(reverse_lazy('export_lsd:config_eb_list'))

    # Debe tener al menos una empresa asociada
    empresa_config_qs = Empresa.objects.filter(user=request.user).order_by('name')

    if not empresa_config_qs:
        messages.error(request, "Debe tener al menos asociada una empresa para ")
        return redirect(reverse_lazy('export_lsd:empresa_list'))

    basic_export_config_json = []
    empresa_config_json = []

    for item in basic_export_config_qs:
        basic_export_config_json.append(item.toJSON())

    for item2 in empresa_config_qs:
        empresa_config_json.append(item2.toJSON())

    context = {
        'basic_export_config': basic_export_config_json,
        'empresa_config': empresa_config_json,
        'error': ''
    }

    if request.method == 'POST':
        try:
            txt_original = request.FILES['txtfile']
            cuit = request.POST.get('selectEmpresa')
            fecha_pago_str = request.POST.get('payDay')
            fecha_pago = datetime.datetime.strptime(fecha_pago_str, '%d/%m/%Y')
            export_config = eval(request.POST.get('selectBasicConfig'))
            print(export_config)

        except ValueError:
            context['error'] = "Formato de archivo incorrecto"
        except Exception as err:
            context['error'] = type(err)

        # 1) Grabo el txt temporalmente
        fs = FileSystemStorage()
        now_str = datetime.datetime.now().strftime('%Y%m%d%H%M')
        fname = f'{request.user.username}_{now_str}.txt'
        file_temp_path = fs.save(f'export_lsd/static/temp/{fname}', txt_original)

        # 2) Proceso el archivo enviando el path como argumento
        txt_final_export_filepath = export_txt(file_temp_path, cuit, fecha_pago, export_config)

        # 3) Elimino el archivo temporal
        fs.delete(file_temp_path)

        # 4) Agrego el path del txt generado al context
        context['txt_export_filepath'] = txt_final_export_filepath

    return render(request, 'export_lsd/export/basic.html', context)


def import_empleados(request):
    result = {
        'error': '',
        'results': '',
        'invalid_data': '',
    }

    if request.method == 'POST':
        # Confirmation button
        if request.POST.get('has_confirmation') == 'Yes':
            data = request.session['all_data']
            bulk_mgr = BulkCreateManager()
            for item in data:
                print(item[0])
                print(item)
                empresa = Empresa.objects.get(cuit=item[0])
                bulk_mgr.add(Empleado(empresa=empresa, leg=item[1], name=item[2], cuil=item[3]))
            bulk_mgr.done()

            return redirect(reverse_lazy('export_lsd:empleado_list'))
        else:
            try:
                result = get_employees(request.FILES['xlsfile'])
            except ValueError:
                result['error'] = "Formato de archivo incorrecto"
            except Exception as err:
                result['error'] = type(err)

            request.session['all_data'] = result['results']

    return render(request, 'export_lsd/export/empleados.html', result)


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
