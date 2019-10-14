from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from objects.serializers import CreateObjectSerializer


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

