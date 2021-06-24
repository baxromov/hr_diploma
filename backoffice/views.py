from io import BytesIO

import qrcode
from PIL import Image, ImageDraw
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files import File
from django.urls import reverse_lazy
from django.views import generic
from telebot import TeleBot

from app import models
from backoffice import forms
from django.contrib.messages.views import SuccessMessageMixin
import os
from project import settings


class MainTemplate(LoginRequiredMixin, generic.ListView):
    queryset = models.Staff.objects.all()
    template_name = 'backoffice/pages/index.html'


class TableTemplate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'backoffice/pages/table/table.html'


# Staff
class StaffListTemplate(LoginRequiredMixin, generic.ListView):
    template_name = 'backoffice/pages/staff/list.html'
    model = models.Staff

    def get_context_data(self, *, object_list=None, **kwargs):
        staff = super(StaffListTemplate, self).get_context_data(**kwargs)
        company = self.request.user.company
        staff['staffs'] = models.Staff.objects.filter(company=company).order_by('-created_at')
        return staff


class StaffUpdate(LoginRequiredMixin, generic.UpdateView, generic.DetailView):
    template_name = 'backoffice/pages/staff/detail.html'
    form_class = forms.StaffModelForm
    model = models.Staff
    context_object_name = 'staff'
    queryset = models.Staff.objects.all()

    def get_success_url(self):
        staff_id = self.kwargs['pk']
        return reverse_lazy('staff-detail', kwargs={'pk': staff_id})

    def form_valid(self, form):
        form.save()
        return super(StaffUpdate, self).form_valid(form)

    def form_invalid(self, form):
        return super(StaffUpdate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        company = self.request.user.company
        ctx['positions'] = models.Position.objects.filter(company=company).order_by('-created_at')
        ctx['departments'] = models.Department.objects.filter(company=company).order_by('-created_at')
        staff_id = self.kwargs.get('pk')
        salary = models.Salary.objects.filter(staff_id=staff_id).last()
        ctx['salary'] = salary
        additional_payment = models.AdditionalPayments.objects.filter(staff_id=staff_id).last()

        return ctx


class StaffCreate(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/staff/create.html'
    model = models.Staff
    form_class = forms.StaffModelForm
    success_url = reverse_lazy('staff')

    def get_context_data(self, **kwargs):
        ctx = super(StaffCreate, self).get_context_data(**kwargs)
        company = self.request.user.company
        ctx['departments'] = models.Department.objects.filter(company=company).order_by('-created_at')
        ctx['positions'] = models.Position.objects.filter(company=company).order_by('-created_at')
        return ctx

    def form_valid(self, form):
        staff = form.save(commit=False)
        company = self.request.user.company
        staff.company = company
        staff.save()
        # ******************************** Qr code generate *****************************
        qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        user_data = {
            'id': staff.id,
        }
        qr_code_image = qrcode.make(user_data)
        canvas = Image.new('RGB', (450, 450), 'white')
        ImageDraw.Draw(canvas)
        canvas.paste(qr_code_image)
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        staff.qr_code.save(f"{staff.first_name}_{staff.last_name}.png", File(buffer), save=False)
        staff.save()
        canvas.close()
        # *****************************************
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(StaffCreate, self).form_invalid(form)


class StaffDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Staff
    form_class = forms.StaffModelForm
    success_url = reverse_lazy('staff')


# Authentication
class LoginPage(LoginView):
    template_name = 'backoffice/regist/login.html'
    success_url = reverse_lazy('backoffice-main')


class Registration(generic.FormView):
    template_name = 'backoffice/regist/registartion.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('backoffice-main')

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
        company = self.request.user.company
        position['positions'] = models.Position.objects.filter(company=company).order_by('-created_at')
        return position


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
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


# Departments
class DepartmentListView(LoginRequiredMixin, generic.ListView):
    template_name = 'backoffice/pages/departments/list.html'
    queryset = models.Department.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(DepartmentListView, self).get_context_data(**kwargs)
        company = self.request.user.company
        ctx['departments'] = models.Department.objects.filter(company=company).order_by('-created_at')
        return ctx


class DepartmentDeleteView(LoginRequiredMixin, generic.DeleteView):
    queryset = models.Department.objects.all()
    form_class = forms.DepartmentsModelForm
    success_message = "deleted..."
    success_url = reverse_lazy('department')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        request.session['name'] = name
        message = request.session['name'] + ' deleted successfully'
        messages.success(self.request, message)
        return super(DepartmentDeleteView, self).delete(request, *args, **kwargs)


class DepartmentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'backoffice/pages/departments/update.html'
    form_class = forms.DepartmentsModelForm
    model = models.Department
    success_url = reverse_lazy('department')

    def form_valid(self, form):
        self.department = form.save(commit=False)
        company = self.request.user.company
        self.department.company = company
        self.department.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(DepartmentUpdateView, self).form_invalid(form)


class DepartmentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/departments/create.html'
    form_class = forms.DepartmentsModelForm
    success_url = reverse_lazy('department')

    def form_valid(self, form):
        self.department = form.save(commit=False)
        questions = self.request.POST.getlist('field_name')
        company = self.request.user.company
        self.department.company = company
        self.department.save()
        for question in questions:
            models.Question.objects.create(question=question, department=self.department)
        return super().form_valid(form)


# Salary
class SalaryListView(LoginRequiredMixin, generic.ListView):
    model = models.Salary
    template_name = 'backoffice/pages/salary/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(SalaryListView, self).get_context_data(**kwargs)
        staff_id = self.kwargs.get('pk')
        ctx['staff'] = models.Staff.objects.get(id=staff_id)
        ctx['salaries'] = models.Salary.objects.filter(staff_id=staff_id).order_by('-id')
        return ctx


class SalaryCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.SalaryModelForm

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('salary', kwargs={'pk': staff_id})

    def form_valid(self, form):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        self.object = form.save(commit=False)
        staff = models.Staff.objects.get(pk=staff_id)
        self.object.staff = staff
        self.object.save()
        return super(SalaryCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SalaryCreateView, self).form_invalid(form)


class SalaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.SalaryModelForm
    model = models.Salary

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('salary', kwargs={'pk': staff_id})


class SalaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    queryset = models.Salary.objects.all()
    form_class = forms.SalaryModelForm
    success_message = "deleted..."

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('salary', kwargs={'pk': staff_id})


# Vacation
class VacationCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/vacation/list.html'
    form_class = forms.VacationModelForm
    model = models.Vacation

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(VacationCreateView, self).get_context_data(**kwargs)
        staff_id = self.kwargs.get('pk')
        company = self.request.user.company
        ctx['staff'] = models.Staff.objects.get(id=staff_id)
        ctx['vacations'] = models.Vacation.objects.filter(staff_id=staff_id)
        ctx['vacation_types'] = models.VacationType.objects.filter(company=company)
        ctx['staff_id'] = staff_id
        return ctx

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('vacation', kwargs={'pk': staff_id})

    def form_valid(self, form):
        print("123")
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        self.object = form.save(commit=False)
        staff = models.Staff.objects.get(pk=staff_id)
        self.object.staff = staff
        self.object.save()
        return super(VacationCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(VacationCreateView, self).form_invalid(form)


class VacationDeleteView(LoginRequiredMixin, generic.DeleteView):
    queryset = models.Vacation.objects.all()
    form_class = forms.VacationModelForm
    success_message = "deleted..."

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('vacation', kwargs={'pk': staff_id})


class VacationUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.VacationModelForm
    model = models.Vacation

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('vacation', kwargs={'pk': staff_id})


# VacationType
class VacationTypeTypeListView(LoginRequiredMixin, generic.ListView):
    template_name = 'backoffice/pages/vacation/vacation_type/list.html'
    model = models.VacationType

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(VacationTypeTypeListView, self).get_context_data(**kwargs)
        company = self.request.user.company
        # staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        # ctx['staff'] = models.Staff.objects.get(id=staff_id)
        prev_page = self.request.META['HTTP_REFERER']
        ctx['prev_page'] = prev_page
        ctx['vacation_types'] = models.VacationType.objects.filter(company=company)
        return ctx


class VacationTypeCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.VacationTypeModelForm
    model = models.VacationType
    success_url = reverse_lazy('vacation_type')

    def form_valid(self, form):
        self.company = form.save(commit=False)
        company = self.request.user.company
        self.company.company = company
        self.company.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(VacationTypeCreateView, self).form_invalid(form)


class VacationTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.VacationType
    form_class = forms.VacationTypeModelForm
    success_url = reverse_lazy('vacation_type')


class VacationTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.VacationType
    form_class = forms.VacationTypeModelForm
    success_url = reverse_lazy('vacation_type')


# AdditionalPayments
class AdditionalPaymentsCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/additional_payments/list.html'
    form_class = forms.AdditionalPaymentsModelForm
    model = models.AdditionalPayments

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(AdditionalPaymentsCreateView, self).get_context_data(**kwargs)
        staff_id = self.kwargs.get('pk')
        company = self.request.user.company
        ctx['staff'] = models.Staff.objects.get(id=staff_id)
        ctx['additional_payments'] = models.AdditionalPayments.objects.filter(staff_id=staff_id)
        ctx['additional_payments_type'] = models.AdditionalPaymentType.objects.filter(company=company)
        ctx['staff_id'] = staff_id
        return ctx

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('additional_payment', kwargs={'pk': staff_id})

    def form_valid(self, form):
        print("123")
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        self.object = form.save(commit=False)
        staff = models.Staff.objects.get(pk=staff_id)
        self.object.staff = staff
        self.object.save()
        return super(AdditionalPaymentsCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(AdditionalPaymentsCreateView, self).form_invalid(form)


class AdditionalPaymentsDeleteView(LoginRequiredMixin, generic.DeleteView):
    queryset = models.AdditionalPayments.objects.all()
    form_class = forms.AdditionalPaymentsModelForm
    success_message = "deleted..."

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('additional_payment', kwargs={'pk': staff_id})


class AdditionalPaymentsUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AdditionalPaymentsModelForm
    model = models.AdditionalPayments

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('additional_payment', kwargs={'pk': staff_id})


# AdditionalPaymentsType
class AdditionalPaymentsTypeListView(LoginRequiredMixin, generic.ListView):
    template_name = 'backoffice/pages/additional_payments/additional_peyments_type/list.html'
    model = models.AdditionalPayments

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(AdditionalPaymentsTypeListView, self).get_context_data(**kwargs)
        company = self.request.user.company
        # staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        # ctx['staff'] = models.Staff.objects.get(id=staff_id)
        prev_page = self.request.META['HTTP_REFERER']
        ctx['prev_page'] = prev_page
        ctx['additional_payments_types'] = models.AdditionalPaymentType.objects.filter(company=company)
        return ctx


class AdditionalPaymentsTypeCreateView(LoginRequiredMixin, generic.CreateView):
    # template_name = 'backoffice/pages/additional_payments/additional_peyments_type/list.html'
    form_class = forms.AdditionalPaymentTypeModelForm
    model = models.AdditionalPayments
    success_url = reverse_lazy('additional_payment_type')

    def form_valid(self, form):
        self.company = form.save(commit=False)
        company = self.request.user.company
        self.company.company = company
        self.company.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(AdditionalPaymentsTypeCreateView, self).form_invalid(form)


class AdditionalPaymentsTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.AdditionalPaymentType
    form_class = forms.AdditionalPaymentTypeModelForm
    success_url = reverse_lazy('additional_payment_type')


class AdditionalPaymentsTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.AdditionalPaymentType
    form_class = forms.AdditionalPaymentTypeModelForm
    success_url = reverse_lazy('additional_payment_type')


# Document
class DocumentListCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/document/list.html'
    form_class = forms.DocumentModelForm
    model = models.Document

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(DocumentListCreateView, self).get_context_data(**kwargs)
        staff_id = self.kwargs.get('pk')
        ctx['documents'] = models.Document.objects.filter(staff_id=staff_id)
        ctx['staff_id'] = staff_id
        return ctx

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('document', kwargs={'pk': staff_id})

    def form_valid(self, form):
        print("123")
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        self.object = form.save(commit=False)
        staff = models.Staff.objects.get(pk=staff_id)
        self.object.staff = staff
        self.object.save()
        return super(DocumentListCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(DocumentListCreateView, self).form_invalid(form)


class DocumentDeleteView(LoginRequiredMixin, generic.DeleteView):
    queryset = models.Document.objects.all()
    form_class = forms.DocumentModelForm
    success_message = "deleted..."

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('document', kwargs={'pk': staff_id})


class DocumentUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.DocumentModelForm
    model = models.Document

    def get_success_url(self):
        staff_id = self.request.META['HTTP_REFERER'].split("/")[-1]
        return reverse_lazy('document', kwargs={'pk': staff_id})


# NewTelegramStaff
class NewTelegramStaffListView(LoginRequiredMixin, generic.ListView):
    template_name = 'backoffice/pages/new-telegram-staff/list.html'
    queryset = models.NewStaff.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(NewTelegramStaffListView, self).get_context_data(**kwargs)
        company = self.request.user.company
        ctx['new_staffs'] = models.NewStaff.objects.filter(company=company)
        return ctx


class NewTelegramStaffDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'backoffice/pages/new-telegram-staff/detail.html'
    queryset = models.NewStaff.objects.all()
    context_object_name = 'new_staff'


# -----------------------------------------------------------------------------------------


# Settings
class Settings(LoginRequiredMixin, generic.TemplateView):
    template_name = 'backoffice/pages/settings/index.html'


# Bot
class BotListView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/bot/list.html'
    queryset = models.Bot.objects.all()
    form_class = forms.BotModelForm
    model = models.Bot
    success_url = reverse_lazy('bot_c_l')

    def generate_bot(self, token, company_id):
        bot_path = str(settings.BASE_DIR) + '/app/sample_bot.py'
        with open(bot_path) as f:
            new_bot = f.read().replace('TOKEN = None', f'TOKEN = "{token}"')

        # bot_conf = str(settings.BASE_DIR) + "/bot/conf/bot_conf.conf"
        # bot_conf_new = "/etc/supervisor/conf.d/bot_conf_{}.conf".format(user_id)

        new_bot_path = str(settings.BASE_DIR) + f'/app/bot/bot_{company_id}.py'
        with open(new_bot_path, "w") as f:
            f.write(new_bot)
        service_config = f"""
[Unit]
Description=uWSGI Emperor service

[Service]
WorkingDirectory=/var/www/hr_project/project
#ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown ubuntu:www-data /run/uwsgi'
ExecStart=/var/www/hr_project/venv/bin/python /var/www/hr_project/project/app/bot/bot_{company_id}.py --serve-in-foreground
Restart=always
KillSignal=SIGQUIT
Type=idle

[Install]
WantedBy=multi-user.target
        """
        with open(f'/etc/systemd/system/bot_{company_id}.service', 'w') as f:
            f.write(service_config)

        # with open(bot_conf) as f:
        #     newText = f.read().replace('[program:bot]', '[program:bot_{}]'.format(user_id))
        #     newText = newText.replace('command=/bot/venv/bin/python /bot/bots/bot_father.py', 'command=/bot/venv/bin/python /bot/bots/bot_{}.py'.format(user_id))
        os.system(f"systemctl daemon-reload")
        os.system(f"systemctl restart bot_{company_id}.service")
        # with open(bot_conf_new, "w") as f:
        #     f.write(newText)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(BotListView, self).get_context_data(**kwargs)
        company = self.request.user.company
        ctx['bot_list'] = models.Bot.objects.filter(company=company).first()
        return ctx

    def form_valid(self, form):
        self.bot = form.save(commit=False)
        company = self.request.user.company
        self.bot.company = company
        self.bot.save()
        token = form.data.get('token')
        self.generate_bot(token, self.bot.company.id)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(BotListView, self).form_invalid(form)


class BotUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.BotModelForm
    model = models.Bot
    success_url = reverse_lazy('bot_c_l')


# Admin
class AdminCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/bot_admin/list.html'
    form_class = forms.AdminModelForm
    model = models.Admin
    success_url = reverse_lazy('admin_bot')

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(AdminCreateView, self).get_context_data(**kwargs)
        company = self.request.user.company
        ctx['admin_lists'] = models.Admin.objects.filter(company=company)
        return ctx

    def form_valid(self, form):
        self.company = form.save(commit=False)
        company = self.request.user.company
        self.company.company = company
        self.company.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(AdminCreateView, self).form_invalid(form)


class AdminDeleteView(LoginRequiredMixin, generic.DeleteView):
    queryset = models.Admin.objects.all()
    form_class = forms.AdminModelForm
    success_message = "deleted..."
    success_url = reverse_lazy('admin_bot')


class AdminUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.AdminModelForm
    model = models.Admin
    success_url = reverse_lazy('admin_bot')


# Admin
class EntryTextCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/entry/list.html'
    form_class = forms.EntryTextModelForm
    model = models.EntryText
    success_url = reverse_lazy('entry_text')

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(EntryTextCreateView, self).get_context_data(**kwargs)
        company = self.request.user.company
        entry_text = models.EntryText.objects.filter(company=company).last()
        ctx['item'] = entry_text
        return ctx

    def form_valid(self, form):
        self.company = form.save(commit=False)
        company = self.request.user.company
        self.company.company = company
        self.company.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(EntryTextCreateView, self).form_invalid(form)


class EntryTextDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    queryset = models.EntryText.objects.all()
    form_class = forms.EntryTextModelForm
    success_message = "deleted..."
    success_url = reverse_lazy('entry_text')


class EntryTextUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.EntryTextModelForm
    model = models.EntryText
    success_url = reverse_lazy('entry_text')


# Company
class CompanyTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'backoffice/pages/company/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(CompanyTemplateView, self).get_context_data(**kwargs)
        ctx['company'] = models.User.objects.get(company=self.request.user.company)
        ctx['item'] = models.Company.objects.get(id=self.request.user.company.id)
        return ctx


class CompanyUpdate(LoginRequiredMixin, generic.UpdateView):
    template_name = 'backoffice/pages/company/update.html'
    form_class = forms.CompanyModelForm
    model = models.Company
    success_url = reverse_lazy('info')


class SearchingStaffListView(LoginRequiredMixin, generic.ListView):
    template_name = 'backoffice/pages/staff_search/list.html'
    model = models.Staff

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(SearchingStaffListView, self).get_context_data(**kwargs)
        ctx['searching_staffs'] = models.Staff.objects.filter(company=self.request.user.company)
        return ctx


# FinishText
class FinishTextCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/finish/list.html'
    form_class = forms.FinishTextModelForm
    model = models.FinishText
    success_url = reverse_lazy('finish_text')

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(FinishTextCreateView, self).get_context_data(**kwargs)
        company = self.request.user.company
        finish_text = models.FinishText.objects.filter(company=company).last()
        ctx['item'] = finish_text
        return ctx

    def form_valid(self, form):
        self.company = form.save(commit=False)
        company = self.request.user.company
        self.company.company = company
        self.company.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(FinishTextCreateView, self).form_invalid(form)


class FinishTextDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    queryset = models.FinishText.objects.all()
    form_class = forms.FinishTextModelForm
    success_message = "deleted..."
    success_url = reverse_lazy('finish_text')


class FinishTexttUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.FinishTextModelForm
    model = models.FinishText
    success_url = reverse_lazy('finish_text')


# Control the flowing staff
class ControlFlowingStaffTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'backoffice/pages/control_flowing_staffs/index.html'


# TrainingInfo
class TrainingInfoTemplateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'backoffice/pages/trainig-info/index.html'
    form_class = forms.TrainingInfoModelForm
    success_url = reverse_lazy('training_info')
    model = models.TrainingInfo

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(TrainingInfoTemplateView, self).get_context_data(**kwargs)
        company = self.request.user.company
        training_info = models.TrainingInfo.objects.filter(company=company)
        staffs = models.Staff.objects.filter(company=company)
        ctx['items'] = training_info
        ctx['staffs'] = staffs
        return ctx

    def form_valid(self, form):
        self.training_info = form.save(commit=False)
        self.training_info.company = self.request.user.company
        self.training_info.save()
        questions = self.request.POST.getlist('field_name')
        position_id = self.request.POST.get('position')
        staffs = self.request.POST.getlist('staff')

        for staff_id in staffs:
            staff = models.Staff.objects.get(id=staff_id)
            staff.traininganswer_set.all().delete()
        for question in questions:
            training_questions = models.TrainingQuestion.objects.create(question=question,
                                                                        position=self.training_info.position)
            for staff_id in staffs:
                traininganswer = models.TrainingAnswer.objects.create()
                staff = models.Staff.objects.get(id=staff_id)
                staff.traininganswer_set.add(traininganswer)

                staff.save()
                training_questions.traininganswer_set.add(traininganswer)
                training_questions.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return super(TrainingInfoTemplateView, self).form_invalid(form)


class TrainingInfoDeleteView(LoginRequiredMixin, generic.DeleteView):
    queryset = models.TrainingInfo.objects.all()
    form_class = forms.TrainingInfoModelForm
    success_message = "deleted..."
    success_url = reverse_lazy('training_info')


class TrainingInfoUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.TrainingInfoModelForm
    model = models.TrainingInfo
    success_url = reverse_lazy('training_info')


# TrainingAnswerListView
class TrainingAnswerListView(LoginRequiredMixin, generic.ListView):
    template_name = 'backoffice/pages/trainig-info/answer.html'
    model = models.Staff

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(TrainingAnswerListView, self).get_context_data(**kwargs)
        company = self.request.user.company
        ctx['staffs'] = models.Staff.objects.filter(company=company)
        ctx['answers'] = models.TrainingAnswer.objects.filter(staff__company=company)
        return ctx
