from django import forms

from finsys.models import LoanHistoryModel, BankModel


class LoanForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LoanForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

        self.fields["date"].widget = forms.DateInput(attrs={'type': 'date', "class": "form-control floating-input"})

    class Meta:
        model = LoanHistoryModel
        exclude = ("balance", "user", "is_deleted")


class LoanPayForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control floating-input'}))
    principle_amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control floating-input', 'type': 'number'}))
    interest = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control floating-input', 'type': 'number'}))
    from_where = forms.ModelChoiceField(queryset=BankModel.objects.all(), widget=forms.Select(attrs={'class': 'form-control floating-input'}))
