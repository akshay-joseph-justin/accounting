from django import forms

from finsys.models import JournalModel, FixedAssetsHistoryModel


class JournalForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control floating-input'}))

    def __init__(self, *args, **kwargs):
        super(JournalForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'

    class Meta:
        model = JournalModel
        exclude = ('is_deleted', 'user', 'history', "is_visible")
