from django import forms

from finsys.models import AccountModel


class BankUpsertForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control floating-input'})

    class Meta:
        model = AccountModel
        fields = ("name",)


class BankDepositForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control floating-input'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control floating-input', 'type': 'number'}))
