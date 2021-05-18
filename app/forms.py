from django import forms

from . import models


class NewCandidateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="To'lliq ism familiyangiz")
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="To'lliq ism familiyangiz")
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control mt-4'}), label="To'lliq ism familiyangiz")

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
