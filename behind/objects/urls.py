from django.urls import path
from objects.views import ObjectCreateView, ObjectAliasView, ObjectRetrieveView

urlpatterns = [
    path('', ObjectCreateView.as_view()),
    path('<name>/', ObjectAliasView.as_view()),
    path('<component>/<type>/<id>/', ObjectRetrieveView.as_view()),
]
