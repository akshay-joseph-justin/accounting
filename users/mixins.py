from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin as BaseFormMixin

from users.models import UserCompanyModel

class FormMixin(BaseFormMixin):
    """
    Form mixin with additional post method
    """

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
