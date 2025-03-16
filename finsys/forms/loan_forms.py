from django import forms

from finsys.models import LoanHistoryModel


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
