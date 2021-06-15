from django.views import generic
from app import forms


# Staff Login
class StaffLoginTemplateView(generic.CreateView):
    template_name = 'app/staff/login.html'
    form_class = forms.StaffLogin

    def form_valid(self, form):
        form = self.form_class(self.request.POST)


# Staff Login
class StaffLoginPageTemplateView(generic.TemplateView):
    template_name = 'app/staff/treining/index.html'

