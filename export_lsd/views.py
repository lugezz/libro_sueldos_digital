import datetime

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView

from export_lsd.models import Empleado, Empresa, Registro
from export_lsd.forms import EmpresaForm, EmpleadoForm


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


def advanced_export(request):

    context = {
        'title': 'Exportación Avanzada',
    }

    return render(request, 'export_lsd/advanced.html', context)


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


class EmpresaFormView(LoginRequiredMixin, FormView):
    form_class = EmpresaForm
    template_name = "export_lsd/empresa/create.html"
    success_url = reverse_lazy("export_lsd:empresa_list")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print(form.is_valid())
        print(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Form | Empresa'
        context['list_url'] = reverse_lazy('export_lsd:empresa_list')
        context['entity'] = 'Empresas'
        context['action'] = 'add'
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
def export_basic(request):
    pass
