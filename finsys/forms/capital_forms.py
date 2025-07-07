from django import forms
from simple_history.utils import update_change_reason

from finsys.models import CapitalHistoryModel, BankModel


class CapitalForm(forms.ModelForm):
    change_reason = forms.CharField(
        help_text="Reason for change",
        widget=forms.TextInput(attrs={'placeholder': 'Enter reason for update'})
    )

    def __init__(self, *args, **kwargs):
        super(CapitalForm, self).__init__(*args, **kwargs)
        print(args, kwargs)

        self.fields["bank"] = forms.ModelChoiceField(queryset=BankModel.objects.filter(company_id=kwargs.get("initial").get("company_id")))
        if not self.instance.pk:
            self.fields.pop('change_reason')

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

        self.fields["date"].widget = forms.DateInput(attrs={'type': 'date', "class": "form-control floating-input"})

    class Meta:
        model = CapitalHistoryModel
        exclude = ("balance", "user", "is_deleted", "is_visible", "company")

    def save(self, commit=True):
        obj = super().save()

        # Capture reason only if it's an update
        if self.instance.pk:
            update_change_reason(obj, self.cleaned_data.get('change_reason'))

        return obj
