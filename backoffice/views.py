from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from app import models
from backoffice import forms


class MainTemplate(LoginRequiredMixin, generic.ListView):
    queryset = models.Staff.objects.all()
    template_name = 'backoffice/pages/index.html'


class TableTemplate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'backoffice/pages/table/table.html'


class StaffListTemplate(LoginRequiredMixin, generic.ListView):
    template_name = 'backoffice/pages/staff/list.html'
    model = models.Staff

    def get_context_data(self, *, object_list=None, **kwargs):
        staff = super(StaffListTemplate, self).get_context_data(**kwargs)
        staff['staffs'] = models.Staff.objects.all().order_by('-created_at')
        return staff


class StaffUpdate(LoginRequiredMixin, generic.UpdateView, generic.DetailView):
    template_name = 'backoffice/pages/staff/detail.html'
    form_class = forms.StaffModelForm
    model = models.Staff
    success_url = reverse_lazy('staff')
    context_object_name = 'staff'
    queryset = models.Staff.objects.all()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


#
# class StaffDetail(LoginRequiredMixin, generic):
#     template_name = 'backoffice/pages/staff/detail.html'
#     queryset = models.Staff.objects.all()
#     context_object_name = 'staff'


# Authentication
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


# Position
class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/department/create.html'
    form_class = forms.PositionModelForm
    success_url = reverse_lazy('position')

    def form_valid(self, form):
        self.position = form.save(commit=False)
        company = self.request.user.company
        self.position.company = company
        self.position.save()
        return super().form_valid(form)


class PositionListView(LoginRequiredMixin, generic.ListView):
    template_name = 'backoffice/pages/department/list.html'
    queryset = models.Position.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        position = super(PositionListView, self).get_context_data(**kwargs)
        position['positions'] = models.Position.objects.all().order_by('-created_at')
        return position


class PositionUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = 'backoffice/pages/department/update.html'
    form_class = forms.PositionModelForm
    model = models.Position
    success_url = reverse_lazy('position')

    def form_valid(self, form):
        self.position = form.save(commit=False)
        company = self.request.user.company
        self.position.company = company
        self.position.save()
        return super().form_valid(form)


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    # template_name = 'backoffice/pages/department/delete.html'
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
