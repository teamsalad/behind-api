from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.views.generic.base import View
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from objects.models import Object
from objects.serializers import CreateObjectSerializer, AliasObjectSerializer, STATE
from purchases.models import Purchase


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
            return Object.objects.get(name=self.kwargs['name'], state=STATE[0][0])
        except Object.DoesNotExist:
            raise Http404()


class ObjectRetrieveView(View):
    def get_object(self):
        try:
            link_alias = f"{self.kwargs['type']}/{self.kwargs['id']}/"
            return Object.objects.get(link_alias=link_alias, state=STATE[1][0])
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
            gifticon_owner = request.user.is_authenticated and Purchase.objects.filter(
                transaction_to=request.user,
                item_type=gifticon_type,
                item_id=kwargs['id']
            ).exists()
            if not gifticon_owner:
                return HttpResponseForbidden()
        return redirect(aliased_object.object.url)
