from rest_framework import serializers

from mailing_list.models import MailList, Client, Tag, OperatorCode, Message, MailListStat


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag"]


class OperatorCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatorCode
        fields = ["operator_code"]


class MailListSerializer(serializers.ModelSerializer):
    # messages = serializers.StringRelatedField(many=True)

    class Meta:
        model = MailList
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class AllStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailListStat
        fields = "__all__"


class StatsSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = MailList
        fields = "__all__"
