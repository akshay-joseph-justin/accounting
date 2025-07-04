from django.contrib.auth.mixins import AccessMixin


class SuperuserRequiredMixin(AccessMixin):
    """
    Require users to be superusers to access the view.
    """

    def dispatch(self, request, *args, **kwargs):
        """Call the appropriate handler if the user is a superuser"""
        if not request.user.is_superuser:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
