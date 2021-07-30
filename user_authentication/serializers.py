from rest_framework import serializers

from .models import UserAuthenticationLogs as UserAuthenticationLogsModel


class UserAuthenticationLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuthenticationLogsModel
        fields = "__all__"
