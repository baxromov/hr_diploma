from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from app import forms
from app import models
import uuid


# Staff Login
class StaffLoginTemplateView(generic.FormView):
    template_name = 'app/staff/login.html'
    form_class = forms.StaffLoginForm
    success_url = 'staff-training'

    def form_valid(self, form):
        print(form)
        staff = models.Staff.objects.get(username=form.data.get('username'))
        staff.training_url = uuid.uuid4()
        self.success_url = reverse('staff_training', kwargs={'staff_uuid': staff.training_url})
        staff.save()
        return super().form_valid(form)


class StaffFormView(generic.FormView):
    template_name = 'app/staff/treining/index.html'
    form_class = forms.StaffTrainingQuestionForm
    success_url = 'staff-login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_uuid = self.kwargs.get('staff_uuid')
        staff = models.Staff.objects.get(training_url=staff_uuid)
        training_answers = models.TrainingAnswer.objects.filter(staff=staff).order_by('id')
        salary = models.Salary.objects.filter(staff=staff).last()
        position = staff.position
        training_info = models.TrainingInfo.objects.filter(position=position).last()
        context['staff'] = staff
        context['salary'] = salary
        context['training_info'] = training_info
        context['training_answers'] = training_answers
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        # return redirect('staff_login')
        return response

    def form_valid(self, form):
        staff_uuid = self.kwargs.get('staff_uuid')
        staff = models.Staff.objects.get(training_url=staff_uuid)
        training_answers = models.TrainingAnswer.objects.filter(staff=staff)
        for training_answer in training_answers:
            training_answer.answer = form.data.get(f'{training_answer.id}')
            training_answer.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


