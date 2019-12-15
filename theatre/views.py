from theatre.models import Room, Movie, Showing
from theatre.serializers import RoomSerializer, MovieSerializer, ShowingSerializer
from rest_framework import generics


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
