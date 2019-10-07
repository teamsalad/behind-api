from django.urls import path
from purchases.views import PurchaseListView, PurchaseBalanceView

urlpatterns = [
    path('', PurchaseListView.as_view()),
    path('balance/', PurchaseBalanceView.as_view()),
]
