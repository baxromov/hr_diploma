from ckeditor.widgets import CKEditorWidget
from django import forms

from app import models


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    company_name = forms.CharField(max_length=255)
    telephone_number = forms.CharField(max_length=20)
    type_of_company_id = forms.IntegerField()
    amount_of_staff = forms.IntegerField(max_value=1000)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput())

    def save(self):
        username = self.cleaned_data['username']
        telephone_number = self.cleaned_data['telephone_number']
        company_name = self.cleaned_data['company_name']
        type_of_company_id = self.cleaned_data['type_of_company_id']
        amount_of_staff = self.cleaned_data['amount_of_staff']
        password = self.cleaned_data['password']
        type_of_company = models.TypeCompany.objects.filter(id=type_of_company_id).first()
        company = models.Company.objects.create(phone=telephone_number, type=type_of_company,
                                                amount_of_staff=amount_of_staff, name=company_name)
        models.User.objects.create_user(username=username, password=password, company=company, is_staff=True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput())


class PositionModelForm(forms.ModelForm):
    class Meta:
        model = models.Position
        exclude = ('company',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'info': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StaffModelForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        exclude = ('company',)


class DepartmentsModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        exclude = ('company',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'info': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SalaryModelForm(forms.ModelForm):
    class Meta:
        model = models.Salary
        exclude = ('staff',)


class VacationModelForm(forms.ModelForm):
    class Meta:
        model = models.Vacation
        exclude = ('staff',)


class VacationTypeModelForm(forms.ModelForm):
    class Meta:
        model = models.VacationType
        exclude = ('company',)


class AdditionalPaymentsModelForm(forms.ModelForm):
    class Meta:
        model = models.AdditionalPayments
        exclude = ('staff',)


class AdditionalPaymentTypeModelForm(forms.ModelForm):
    class Meta:
        model = models.AdditionalPaymentType
        exclude = ('company',)


class DocumentModelForm(forms.ModelForm):
    class Meta:
        model = models.Document
        exclude = ('staff',)


class BotModelForm(forms.ModelForm):
    class Meta:
        model = models.Bot
        exclude = ('company',)


class AdminModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        exclude = ('company',)


class EntryTextModelForm(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.EntryText
        exclude = ('company',)


class FinishTextModelForm(forms.ModelForm):
    class Meta:
        model = models.FinishText
        exclude = ('company',)


class TrainingInfoModelForm(forms.ModelForm):
    class Meta:
        model = models.TrainingInfo
        exclude = ('company',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CompanyModelForm(forms.ModelForm):
    class Meta:
        model = models.Company
        exclude = ('company',)


class CompanyCultureModelForm(forms.ModelForm):
    class Meta:
        model = models.CompanyCulture
        exclude = ('company',)
