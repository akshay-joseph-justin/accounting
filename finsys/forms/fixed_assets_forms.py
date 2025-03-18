from django import forms

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


class DepreciationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DepreciationForm, self).__init__(*args, **kwargs)
        self.fields["depreciation"].widget = forms.DateInput(
            attrs={'type': 'number', "class": "form-control floating-input"})

    class Meta:
        model = FixedAssetsHistoryModel
        fields = ("depreciation",)
