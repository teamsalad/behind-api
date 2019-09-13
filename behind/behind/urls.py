"""behind URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from companies.views import (
    UserJobHistoryListView,
    UserJobHistoryConfirmView,
    CompanyListView,
    JobListView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/users/', include('rest_framework.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/user-job-histories/', UserJobHistoryListView.as_view()),
    re_path(r'^api/v1/user-job-histories/confirm-email/(?P<key>[-:\w]+)/$',
            UserJobHistoryConfirmView.as_view(),
            name='confirm_company_email'),
    path('api/v1/companies/', CompanyListView.as_view()),
    path('api/v1/jobs/', JobListView.as_view()),
]
