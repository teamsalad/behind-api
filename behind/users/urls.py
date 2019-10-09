from allauth.account.views import confirm_email, email_verification_sent
from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_auth.registration.views import RegisterView
from rest_auth.views import (
    PasswordResetView,
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView
)

from users.views import UserPasswordResetConfirmView

urlpatterns = [
    # URLs that do not require a session or valid token
    path('password/reset/', PasswordResetView.as_view(),
         name='rest_password_reset'),
    path('password/reset/confirm/', UserPasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),
    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            TemplateView.as_view(template_name="password/password_reset_confirm.html"),
            name='password_reset_confirm'),
    path('login/', LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('password/change/', PasswordChangeView.as_view(),
         name='rest_password_change'),
    # URLs for user registration
    path('registration/', RegisterView.as_view(), name='rest_register'),
    path('registration/confirm-email/',
         email_verification_sent,
         name='account_email_verification_sent'),
    re_path(r'^registration/confirm-email/(?P<key>[-:\w]+)/$',
            confirm_email,
            name='account_confirm_email'),
]
