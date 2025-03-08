from django.views.generic import DeleteView as BaseDeleteView


class DeleteView(BaseDeleteView):

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
