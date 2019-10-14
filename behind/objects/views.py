from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from objects.models import Object
from objects.serializers import CreateObjectSerializer, AliasObjectSerializer, STATE


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
