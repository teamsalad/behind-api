from django.urls import path
from purchases.views import PurchaseListView

urlpatterns = [
    path('', PurchaseListView.as_view()),
]
