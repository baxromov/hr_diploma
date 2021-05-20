from django.contrib.auth import get_user_model
from rest_framework import serializers

from app import models

UserModel = get_user_model()


class FlowModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Flow
        exclude = ()


class StaffModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Staff
        exclude = ()
