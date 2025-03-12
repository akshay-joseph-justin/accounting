from django import forms

from finsys.models import JournalEntryModel, JournalEntryLineModel


class JournalEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JournalEntryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

    class Meta:
        model = JournalEntryModel
        fields = ['date', 'reference_number']


class JournalEntryLineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JournalEntryLineForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

    class Meta:
        model = JournalEntryLineModel
        fields = ['account', 'entry_type', 'amount']


JournalEntryLineFormSet = forms.inlineformset_factory(
    JournalEntryModel,
    JournalEntryLineModel,
    form=JournalEntryLineForm,
    extra=2,
    can_delete=True
)