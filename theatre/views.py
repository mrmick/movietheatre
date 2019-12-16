from theatre.models import Room, Movie, Showing, Ticket
from theatre.serializers import RoomSerializer, MovieSerializer, ShowingSerializer, ShowingDetailSerializer, \
    TicketSerializer, TicketDetailSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response


# Create your views here.
class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ShowingList(generics.ListCreateAPIView):
    queryset = Showing.objects.all()
    serializer_class = ShowingSerializer


class ShowingDetail(generics.RetrieveUpdateAPIView):
    queryset = Showing.objects.all()
    serializer_class = ShowingDetailSerializer
    lookup_field = 'pk'

    def get_object(self):
        return get_object_or_404(Showing, pk=self.kwargs['pk'])


class ShowingTicket(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TicketDetailSerializer
        else:
            return TicketSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(showing=self.kwargs['pk'])
        return queryset

    def perform_create(self, serializer):
        showing = get_object_or_404(
            Showing, pk=self.kwargs.get('pk')
        )
        serializer.save(showing=showing)


class TicketDetail(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketDetailSerializer
    lookup_field = 'pk'

    def get_object(self):
        return get_object_or_404(Ticket, pk=self.kwargs['pk'])

