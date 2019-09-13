from django.urls import path, re_path, include
from allauth.account.views import confirm_email, email_verification_sent
from rest_auth.registration.views import RegisterView

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', RegisterView.as_view(), name='rest_register'),
    path('registration/confirm-email/',
         email_verification_sent,
         name='account_email_verification_sent'),
    re_path(r'^registration/confirm-email/(?P<key>[-:\w]+)/$',
            confirm_email,
            name='account_confirm_email'),
]
