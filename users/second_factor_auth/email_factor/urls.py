from django.urls import path

from . import views

urlpatterns = [
    path("send/otp/<token>/", views.SendOTPView.as_view(), name="email-factor"),
    path("resend/otp/", views.ResendOTPView.as_view(), name="resend-email-factor"),
    path("verify/<token>", views.VerifyOTP.as_view(), name="email-factor-verify"),
]
