from django import forms

from . import models


class AccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.AccountModel
        exclude = ['is_active', 'balance']


class JournalEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JournalEntryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.JournalEntry
        fields = ['date', 'reference_number', 'description', 'period']


class JournalEntryLineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JournalEntryLineForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.JournalEntryLineModel
        fields = ['account', 'description', 'debit_amount', 'credit_amount']


class JournalEntryLineFormset(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()

        total_debit = 0
        total_credit = 0
        valid_forms = 0  # Ensure at least one valid form is submitted

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):  # Ignore deleted forms

                if not form.cleaned_data.get("debit_amount") and not form.cleaned_data.get("credit_amount"):
                    raise forms.ValidationError("debit or credit amount must be set")

                if form.cleaned_data.get("debit_amount") and form.cleaned_data.get("credit_amount"):
                    raise forms.ValidationError("Line item cannot have both debit and credit amounts")

                valid_forms += 1
                total_debit += form.cleaned_data.get("debit_amount", 0)
                total_credit += form.cleaned_data.get("credit_amount", 0)

        # Ensure at least one valid form exists
        if valid_forms < 2:
            raise forms.ValidationError("At least two entries are required.")

        # Ensure total debits equal total credits
        if total_debit != total_credit:
            raise forms.ValidationError("Total debit must equal total credit.")


JournalEntryLineFormSet = forms.inlineformset_factory(
    models.JournalEntry,
    models.JournalEntryLineModel,
    form=JournalEntryLineForm,
    formset=JournalEntryLineFormset,
    extra=2,
    can_delete=True
)
