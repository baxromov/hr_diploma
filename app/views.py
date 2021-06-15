from django.views import generic
from app import forms


# Staff Login
class StaffLoginTemplateView(generic.FormView):
    template_name = 'app/staff/login.html'
    form_class = forms.StaffLogin
    success_url = 'staff-training'

    def form_valid(self, form):
        return super().form_valid(form)


# Staff Login
class StaffLoginPageTemplateView(generic.TemplateView):
    template_name = 'app/staff/treining/index.html'

