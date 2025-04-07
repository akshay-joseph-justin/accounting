from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.views.generic import View


class DeleteView(View):
    model = None
    success_url = None

    def get_model(self):
        if self.model:
            return self.model
        raise ImproperlyConfigured('You must define a model attribute')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        raise ImproperlyConfigured('You must define a success_url attribute')

    def delete(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            raise ImproperlyConfigured('You must specify a primary key - pk')

        model = self.get_model()
        queryset = model.objects.filter(pk=kwargs['pk']).first()
        queryset.is_deleted = True
        queryset.save()
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        model = self.get_model()
        if not hasattr(model, 'is_deleted'):
            raise ImproperlyConfigured('model has no attribute \'is_deleted\'')
        return self.delete(request, *args, **kwargs)