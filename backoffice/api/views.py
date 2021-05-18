from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from . import serializers
from app import models
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class FlowModelViewSet(viewsets.ModelViewSet):
    queryset = models.Flow.objects.all()
    serializer_class = serializers.FlowModelSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = serializers.UserModelSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = models.User.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=user)
        response = {
            'token': token.key
        }
        return Response(response, status=status.HTTP_200_OK)
