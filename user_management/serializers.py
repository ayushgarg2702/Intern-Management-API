from rest_framework import serializers

from .models import (
    UserDetails as UserDetailsModel,
)


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailsModel
        fields = "__all__"