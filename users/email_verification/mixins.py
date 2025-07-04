from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class EmailVerificationRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified():
            messages.info(request, "Email verification required")
            return redirect(reverse_lazy("users:verification-email-redirect"))
        return super().dispatch(request, *args, **kwargs)