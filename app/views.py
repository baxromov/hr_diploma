from django.views import generic


# Staff Login
class StaffLoginTemplateView(generic.TemplateView):
    template_name = 'app/staff/login.html'
