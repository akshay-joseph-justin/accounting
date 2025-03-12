from django import forms

from finsys.models import AccountModel


class BankForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control floating-input'})

    class Meta:
        model = AccountModel
        fields = ("name",)
