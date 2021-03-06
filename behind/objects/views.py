from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from behind import settings
from objects.models import Object
from objects.serializers import CreateObjectSerializer, AliasObjectSerializer, STATE as OBJECT_STATE
from purchases.models import Purchase, STATE as PURCHASE_STATE


class ObjectCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateObjectSerializer

    def post(self, request, format=None, **kwargs):
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


class ObjectAliasView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AliasObjectSerializer

    def get_object(self):
        try:
            return Object.objects.get(name=self.kwargs['name'], state=OBJECT_STATE[0][0])
        except Object.DoesNotExist:
            raise Http404()


class ObjectRetrieveView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        try:
            link_alias = f"{self.kwargs['type']}/{self.kwargs['id']}/"
            return Object.objects.get(link_alias=link_alias, state=OBJECT_STATE[1][0])
        except Object.DoesNotExist:
            raise Http404()

    def get(self, request, *args, **kwargs):
        aliased_object = self.get_object()
        if kwargs['type'] == 'gifticons':
            # Check if user is gifticon owner
            gifticon_type = ContentType.objects.get(
                app_label='rewards',
                model='gifticon'
            )
            gifticon_owner = Purchase.objects.filter(
                transaction_from=request.user,
                transaction_to_id=settings.TRANSACTION_STAGING_ACCOUNT_ID,
                item_type=gifticon_type,
                item_id=kwargs['id'],
                state=PURCHASE_STATE[1][0]
            ).exists()
            if not gifticon_owner:
                return HttpResponseForbidden()
        return HttpResponseRedirect(aliased_object.object.url)
