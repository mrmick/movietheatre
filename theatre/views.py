from theatre.models import Room, Movie, Showing
from theatre.serializers import RoomSerializer, MovieSerializer, ShowingSerializer, ShowingDetailSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404


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