from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from purchases.models import Purchase
from purchases.serializers import CreatePurchaseSerializer, PurchaseSerializer


class PurchaseListView(ListAPIView):
    """
    List my purchase history
    Purchase an item (answer, payment)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(
            Q(transaction_from=self.request.user.id) |
            Q(transaction_to=self.request.user.id)
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePurchaseSerializer
        return PurchaseSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PurchaseBalanceView(GenericAPIView):
    """
    Get my point balance
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        return Response({'balance': request.user.balance()})
