from django.urls import path
from objects.views import ObjectCreateView, ObjectAliasView

urlpatterns = [
    path('', ObjectCreateView.as_view()),
    path('<name>/', ObjectAliasView.as_view()),
]
