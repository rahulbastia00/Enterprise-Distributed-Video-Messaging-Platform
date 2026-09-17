from rest_framework import generics
from .models import Channel, Message
from .serializers import ChannelSerializer, MessageSerializer

class ChannelListCreateView(generics.ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    def perform_create(self, serializer):
        channel = serializer.save()
        channel.members.add(self.request.user)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        channel_id = self.kwargs['channel_id']
        return Message.objects.filter(channel_id=channel_id)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)