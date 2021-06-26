from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt import serializers as rest_framework_simplejwt_serializers
from rest_framework_simplejwt.serializers import TokenVerifySerializer

from app import models

UserModel = get_user_model()


class FlowParentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Staff
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
        )


class FlowModelSerializer(serializers.ModelSerializer):

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     # response['child'] = ChildSerializer(instance.child).data
    #     response['staff'] = FlowParentModelSerializer(self.context['request'].user.company.staff_set.all()).data
    #     return response

    class Meta:
        model = models.Flow
        fields = '__all__'
        # exclude = ()


class StaffModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Staff
        exclude = ()


class JWTTokenObtainSerializer(rest_framework_simplejwt_serializers.TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class JWTTokenVerifySerializer(rest_framework_simplejwt_serializers.TokenVerifySerializer):

    def validate(self, attrs):
        data = rest_framework_simplejwt_serializers.UntypedToken(attrs['token'])
        user_id = data.payload.get('user_id', False)
        valid_data = TokenVerifySerializer().validate(data)
        user = models.Staff.objects.get(id=user_id)

        user_serializers = StaffModelSerializer(user)
        return {
            'status': 'success',
            'data': {
                "valid": True,
                "user": user_serializers.data
            },
        }
