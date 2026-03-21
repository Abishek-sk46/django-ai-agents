from rest_framework import serializers


class AgentQuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False, allow_null=True)
    message = serializers.CharField(required=True)
    context = serializers.DictField(required=False, default=dict)
    constraints = serializers.DictField(required=False, default=dict)