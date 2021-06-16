from django import forms
from django.core.exceptions import ValidationError

from . import models


class NewCandidateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="To'lliq ism familiyangiz")
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label="To'lliq ism familiyangiz")
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control mt-4'}),
                             label="To'lliq ism familiyangiz")

    class Meta:
        model = models.NewStaff
        fields = [
            'full_name',
            'birth_date',
            'image',
            # 'position',
        ]


class AnswerModelForm(forms.ModelForm):
    # candidates = NewCandidateForm()

    class Meta:
        model = models.Answer
        fields = [
            'candidate',
            'question',
            'answer',
        ]


class StaffLoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=55, required=True)

    def clean_username(self):
        username = self.data.get('username')
        if not models.Staff.objects.filter(username=username).exists():
            raise ValidationError('Staff not found!')
        return username

    def clean_password(self):
        username = self.data.get('username')
        password = self.data.get('password')
        staff = models.Staff.objects.filter(username=username).first()
        if not staff.password == password:
            raise ValidationError('Password is incorrect')
        return username


class StaffTrainingQuestionForm(forms.Form):
    pass
