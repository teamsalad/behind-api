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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from behind import settings
from companies.views import CompanyListView, JobListView
from questions.views import (
    QuestionListView,
    QuestionDetailView,
    AnswerListView,
    AnswerDetailView,
    QuestionFeedView,
)
from settings.views import PushNotificationSettingView, AppVersionView

admin.site.site_header = "The Behind Administration"
admin.site.site_title = "Welcome to Behind Administration"
admin.site.index_title = "Behind Entity Management"

router = DefaultRouter()
router.register(r'devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('api/v1/', include(router.urls)),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/users/push-notification-settings/', PushNotificationSettingView.as_view()),
    path('api/v1/user-job-histories/', include('companies.urls')),
    path('api/v1/companies/', CompanyListView.as_view()),
    path('api/v1/jobs/', JobListView.as_view()),
    path('api/v1/questions/', QuestionListView.as_view()),
    path('api/v1/questions/<int:id>/', QuestionDetailView.as_view()),
    path('api/v1/questions/feed/', QuestionFeedView.as_view()),
    path('api/v1/answers/', AnswerListView.as_view()),
    path('api/v1/answers/<int:id>/', AnswerDetailView.as_view()),
    path('api/v1/chat_rooms/', include('chats.urls')),
    path('api/v1/purchases/', include('purchases.urls')),
    path('api/v1/app-version/<device_type>/', AppVersionView.as_view()),
    path('api/v1/objects/', include('objects.urls')),
    path('_/health/', include('health_check.urls')),
    path('_/admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('api/docs/users/', include('rest_framework.urls')),
    ] + urlpatterns
