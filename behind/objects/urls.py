from django.urls import path
from objects.views import ObjectCreateView

urlpatterns = [
    path('', ObjectCreateView.as_view()),
]
