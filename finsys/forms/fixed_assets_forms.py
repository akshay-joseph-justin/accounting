from django import forms
from simple_history.utils import update_change_reason

from finsys.models import FixedAssetsHistoryModel


class FixedAssetsCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FixedAssetsCreateForm, self).__init__(*args, **kwargs)

        self.fields["from_where"].label = "Asset Name"

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

        self.fields["date"].widget = forms.DateInput(attrs={'type': 'date', "class": "form-control floating-input"})

    class Meta:
        model = FixedAssetsHistoryModel
        exclude = ("balance", "user", "is_deleted", "depreciation", "current_balance", "is_visible")

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount > self.cleaned_data["bank"].balance or self.cleaned_data["current_balance"] > self.cleaned_data[
            "bank"].balance:
            raise forms.ValidationError("amount is greater than bank balance")
        return amount


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
        exclude = ("balance", "user", "is_deleted", "current_balance", "depreciation", "is_visible")

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount > self.cleaned_data["bank"].balance or self.cleaned_data["current_balance"] > self.cleaned_data[
            "bank"].balance:
            raise forms.ValidationError("amount is greater than bank balance")
        return amount

    def save(self, commit=True):
        obj = super().save(commit=False)

        # Capture reason only if it's an update
        if self.instance.pk:
            update_change_reason(obj, self.cleaned_data.get('change_reason'))

        if commit:
            obj.save()
        return obj
