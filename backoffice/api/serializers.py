from rest_framework import serializers
from app import models
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

UserModel = get_user_model()


class FlowModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flow
        exclude = ()


class UserModelSerializers(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    branch_id = serializers.IntegerField(required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        branch_id = data.get('branch_id')

        if username is None:
            raise serializers.ValidationError(
                'An username address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        if branch_id is None:
            raise serializers.ValidationError(
                'A Branch id is required to log in.'
            )

        if not models.User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Not found username")

        if not models.User.objects.filter(branch_id=branch_id).exists():
            raise serializers.ValidationError("Not found branch id")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("The password fields didn't match.")

        return data

    class Meta:
        model = UserModel
        fields = [
            'username',
            'password',
            'branch_id'
        ]
