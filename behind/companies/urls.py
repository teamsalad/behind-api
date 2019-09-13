from django.urls import path, re_path
from companies.views import (
    UserJobHistoryListView,
    UserJobHistoryConfirmView,
)

urlpatterns = [
    path('', UserJobHistoryListView.as_view()),
    re_path(r'^confirm-email/(?P<key>[-:\w]+)/$',
            UserJobHistoryConfirmView.as_view(),
            name='confirm_company_email'),
]
