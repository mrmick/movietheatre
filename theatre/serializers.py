from theatre.models import Room, Movie, Showing
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
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Showing
        fields = ['id', 'room', 'movie', 'showtime', 'sold_seats', 'available_seats', 'tickets']
        read_only_fields = ['id', 'room', 'movie', 'showtime', 'sold_seats', 'available_seats']

    def get_tickets(self, obj):
        return None

    def update(self, instance, validated_data):
        tickets = validated_data.get('tickets')
        if instance.available_seats >= tickets:
            instance.sold_seats += tickets
        instance.save()
        return instance