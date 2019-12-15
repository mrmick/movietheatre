from theatre.models import Room, Movie, Showing
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'seats_capacity']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title']


class ShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showing
        fields = ['id', 'room', 'movie', 'showtime', 'sold_seats']
