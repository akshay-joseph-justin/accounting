from django import forms

from finsys.models import JournalModel


class JournalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JournalForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

    class Meta:
        model = JournalModel
        exclude = ('is_deleted', 'user', 'history')
