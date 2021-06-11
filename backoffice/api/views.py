from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from app import models
from . import serializers
from rest_framework import permissions

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutAPIView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class FlowModelViewSet(viewsets.ModelViewSet):
    queryset = models.Flow.objects.all()
    serializer_class = serializers.FlowModelSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['GET', 'POST']


class StaffRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffModelSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        company = self.request.user.company
        staff = models.Staff.objects.filter(company=company)
        serializer = self.get_serializer(staff, many=True)
        return Response(serializer.data)



class JWTTokenObtainView(rest_framework_simplejwt_views.TokenObtainPairView):
    serializer_class = serializers.JWTTokenObtainSerializer


class JWTTokenVerifyView(rest_framework_simplejwt_views.TokenVerifyView):
    serializer_class = serializers.JWTTokenVerifySerializer


class JWTTokenRefreshView(rest_framework_simplejwt_views.TokenRefreshView):
    pass


