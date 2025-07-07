from django import forms
from django.contrib.auth import get_user_model

from users import models


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = models.CompanyModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompanyCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'


class MemberCreateForm(forms.ModelForm):
    class Meta:
        model = models.UserCompanyModel
        fields = ("user", "role")

    def __init__(self, *args, **kwargs):
        super(MemberCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'


class MemberRoleChangeForm(forms.ModelForm):
    class Meta:
        model = models.UserCompanyModel
        fields = ("role",)

    def __init__(self, *args, **kwargs):
        super(MemberRoleChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control floating-input'