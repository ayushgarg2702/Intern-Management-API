from rest_framework import serializers

from .models import UserAttendanceLogs as UserAttendanceLogsModel


class UserAttendanceLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAttendanceLogsModel
        fields = "__all__"

