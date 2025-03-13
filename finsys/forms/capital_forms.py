from django import forms

from finsys.models import AccountModel


class CapitalForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', "class": "form-control floating-input"}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'type': 'number', "class": "form-control floating-input"}))
    bank = forms.ModelChoiceField(queryset=AccountModel.objects.filter(is_bank=True), widget=forms.Select(attrs={'class': 'form-control floating-input'}))
