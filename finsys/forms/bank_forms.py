from django import forms

from finsys.models import BankModel, BankTransactionModel


class BankUpsertForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control floating-input'})
        self.fields['account_number'].widget.attrs.update({'class': 'form-control floating-input'})
        self.fields['branch'].widget.attrs.update({'class': 'form-control floating-input'})

    class Meta:
        model = BankModel
        fields = ("name", "account_number", "branch")


class BankDepositForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control floating-input'}))
    from_where = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control floating-input'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control floating-input', 'type': 'number'}))


class BankTransferForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control floating-input'}))
    from_where = forms.ModelChoiceField(queryset=BankModel.objects.all(), widget=forms.Select(attrs={'class': 'form-control floating-input'}))
    to = forms.ModelChoiceField(queryset=BankModel.objects.all(), widget=forms.Select(attrs={'class': 'form-control floating-input'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control floating-input'}))
