from django.views import generic


# Staff Login
class StaffLoginTemplateView(generic.TemplateView):
    template_name = 'app/staff/login.html'

    def get(self, request, *args, **kwargs):
        # username
        # pass
        staff.check_
        return super().get(request, *args, **kwargs)


# Staff Login
class StaffLoginPageTemplateView(generic.TemplateView):
    template_name = 'app/staff/treining/index.html'

