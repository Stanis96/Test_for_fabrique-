from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response

from mailing_list.models import MailList, Client, Message, Tag, OperatorCode, MailListStat
from mailing_list.serializers import (
    MailListSerializer,
    ClientSerializer,
    MessageSerializer,
    TagSerializer,
    OperatorCodeSerializer,
    AllStatsSerializer,
    StatsSerializer,
)


class MailListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = MailList.objects.all()
    serializer_class = MailListSerializer


class ClientViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
    mixins.DestroyModelMixin,
):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class OperatorCodeViewSet(viewsets.ModelViewSet):
    queryset = OperatorCode.objects.all()
    serializer_class = OperatorCodeSerializer


class AllStatsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = AllStatsSerializer

    def list(self, request, **kwargs):
        mail_lists = []
        for mail_list in MailList.objects.all():
            stat = MailListStat.get_stat_by_id(mail_list_id=mail_list.id)
            mail_lists.append(stat)
        serializer = AllStatsSerializer(mail_lists, many=True)
        return Response(serializer.data)


class StatsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = MailList.objects.all()

    serializer_class = StatsSerializer
