import requests
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from backoffice import forms
from app import models


class MainTemplate(generic.TemplateView):
    template_name = 'backoffice/pages/index.html'


class StaffListTemplate(generic.TemplateView):
    template_name = 'backoffice/pages/staff/list.html'


class StaffDetailTemplate(generic.TemplateView):
    template_name = 'backoffice/pages/staff/detail.html'


class TableTemplate(generic.TemplateView):
    template_name = 'backoffice/pages/table/table.html'


class Login(generic.TemplateView):
    template_name = 'backoffice/regist/login.html'


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
