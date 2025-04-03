from django import forms
from simple_history.utils import update_change_reason

from finsys.models import FixedAssetsHistoryModel


class FixedAssetsCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FixedAssetsCreateForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

        self.fields["date"].widget = forms.DateInput(attrs={'type': 'date', "class": "form-control floating-input"})

    class Meta:
        model = FixedAssetsHistoryModel
        exclude = ("balance", "user", "is_deleted", "depreciation", "current_balance")


class FixedAssetsUpdateForm(forms.ModelForm):
    change_reason = forms.CharField(
        help_text="Reason for change",
        widget=forms.TextInput(attrs={'placeholder': 'Enter reason for update'})
    )

    def __init__(self, *args, **kwargs):
        super(FixedAssetsUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

        self.fields["date"].widget = forms.DateInput(attrs={'type': 'date', "class": "form-control floating-input"})

    class Meta:
        model = FixedAssetsHistoryModel
        exclude = ("balance", "user", "is_deleted", "current_balance", "depreciation")

    def save(self, commit=True):
        obj = super().save(commit=False)

        # Capture reason only if it's an update
        if self.instance.pk:
            update_change_reason(obj, self.cleaned_data.get('change_reason'))

        if commit:
            obj.save()
        return obj
