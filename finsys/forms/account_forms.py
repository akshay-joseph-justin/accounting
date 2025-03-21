from django import forms

from finsys.models import AccountModel, AccountHistoryModel


class AccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

    class Meta:
        model = AccountModel
        exclude = ['is_bank', 'balance', 'is_inbuilt']


class AccountHistoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AccountHistoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

        self.fields["date"].widget = forms.DateInput(attrs={'type': 'date', "class": "form-control floating-input"})

    class Meta:
        model = AccountHistoryModel
        exclude = ("balance", "user", "is_deleted", "from_where", "account")
