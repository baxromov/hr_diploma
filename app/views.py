from django.views import generic
from app import forms
from app import models


# Staff Login
class StaffLoginTemplateView(generic.FormView):
    template_name = 'app/staff/login.html'
    form_class = forms.StaffLogin
    success_url = 'staff-training'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        if form.is_valid():
            pass
        return super().form_valid(form)


# Staff Login
class StaffPageTemplateView(generic.TemplateView):
    template_name = 'app/staff/treining/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(StaffPageTemplateView, self).get_context_data(**kwargs)
        return ctx
