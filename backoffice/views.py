from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic

from app import models
from backoffice import forms


class MainTemplate(LoginRequiredMixin, generic.ListView):
    queryset = models.Staff.objects.all()
    template_name = 'backoffice/pages/index.html'


class StaffListTemplate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'backoffice/pages/staff/list.html'


class StaffDetailTemplate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'backoffice/pages/staff/detail.html'


class TableTemplate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'backoffice/pages/table/table.html'


class LoginPage(LoginView):
    template_name = 'backoffice/regist/login.html'
    success_url = reverse_lazy('backoffice-main')


class Registration(generic.FormView):
    template_name = 'backoffice/regist/registartion.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        response = super(Registration, self).get_context_data(**kwargs)
        response['types'] = models.TypeCompany.objects.all()
        return response

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class PositionCreateView(generic.CreateView):
    template_name = 'backoffice/pages/department/create.html'
    form_class = forms.PositionModelForm


class PositionListView(generic.ListView):
    template_name = 'backoffice/pages/department/list.html'
    queryset = models.Position.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        position = super(PositionListView, self).get_context_data(**kwargs)
        position['positions'] = models.Position.objects.all().order_by('-created_at')
        return position


class PositionUpdateView(generic.UpdateView):
    template_name = 'backoffice/pages/department/update.html'
    queryset = models.Position.objects.all()
    form_class = forms.PositionModelForm


class PositionDeleteView(generic.DeleteView):
    template_name = 'backoffice/pages/department/delete.html'
    queryset = models.Position.objects.all()
    form_class = forms.PositionModelForm
    success_message = "deleted..."
    success_url = '/backoffice/position'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        request.session['name'] = name  # name will be change according to your need
        message = request.session['name'] + ' deleted successfully'
        messages.success(self.request, message)
        return super(PositionDeleteView, self).delete(request, *args, **kwargs)
