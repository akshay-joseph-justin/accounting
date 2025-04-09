from django import forms
from simple_history.utils import update_change_reason

from finsys.models import LoanHistoryModel, BankModel


class LoanForm(forms.ModelForm):
    change_reason = forms.CharField(
        help_text="Reason for change",
        widget=forms.TextInput(attrs={'placeholder': 'Enter reason for update'})
    )

    def __init__(self, *args, **kwargs):
        super(LoanForm, self).__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields.pop('change_reason')

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

        self.fields["date"].widget = forms.DateInput(attrs={'type': 'date', "class": "form-control floating-input"})

    class Meta:
        model = LoanHistoryModel
        exclude = ("balance", "user", "is_deleted", "pending_amount", "is_pay", 'is_visible')

    def save(self, commit=True):
        obj = super().save()

        # Capture reason only if it's an update
        if self.instance.pk:
            update_change_reason(obj, self.cleaned_data.get('change_reason'))
        return obj


class LoanPayForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control floating-input'}))
    principle_amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control floating-input', 'type': 'number'}))
    interest = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control floating-input', 'type': 'number'}))
    from_where = forms.ModelChoiceField(queryset=BankModel.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control floating-input'}))
