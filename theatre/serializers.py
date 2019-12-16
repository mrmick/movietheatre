from theatre.models import Room, Movie, Showing, Ticket
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'name', 'seats_capacity']

    def validate_name(self, value):
        """
        Here's where we check that required fields are included
        """
        if len(value.strip()) < 1:
            raise serializers.ValidationError("{'name': 'required'}")
        return value

    def validate_seats_capacity(self, value):
        """
        Here's where we check that required fields are included
        """
        if value < 1:
            raise serializers.ValidationError("'seats_capacity': 'required'}")
        return value


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id', 'title']

    def validate_title(self, value):
        """
        Here's where we check that required fields are included
        """
        if len(value) < 1:
            raise serializers.ValidationError("{'title': 'required'}")
        return value


class ShowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Showing
        fields = ['id', 'room', 'movie', 'showtime', 'seats_available']
        read_only_fields = ['seats_available']


class ShowingDetailSerializer(serializers.ModelSerializer):
    room = serializers.CharField(source='room.name')
    movie = serializers.CharField(source='movie.title')
    showtime = serializers.DateTimeField(format="%d/%m/%Y, %H:%M")

    class Meta:
        model = Showing
        fields = ['id', 'room', 'movie', 'showtime', 'sold_seats', 'available_seats']
        read_only_fields = ['id', 'room', 'movie', 'showtime', 'sold_seats', 'available_seats']


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['id', 'showing']


class TicketDetailSerializer(serializers.ModelSerializer):

    showing = ShowingSerializer()

    class Meta:
        model = Ticket
        fields = ['id', 'showing']