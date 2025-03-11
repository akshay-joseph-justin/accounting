from django import forms

from finsys.models import BanKModel, BankTransactionModel


class BankForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BankForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

    class Meta:
        model = BanKModel
        fields = ('name',)


class BankTransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BankTransactionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

    class Meta:
        model = BankTransactionModel
        exclude = ('user',)