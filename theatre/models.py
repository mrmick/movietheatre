from django.db import models
from django.utils import timezone


# Create your models here.
class Room(models.Model):
    """
    This is the room in which we will be showing movies.

    The seating is specified as part of its definition and all admission is general admission.
    """
    name = models.CharField(max_length=50)
    seats_capacity = models.IntegerField()

    def __str__(self):
        return f'{self.name} ({self.seats_capacity} seats)'


class Movie(models.Model):
    """
    Represents a Movie.  We only need the title at this time.
    """
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Showing(models.Model):
    """
    Represents a 'showing' of a movie with references to the room and movie.
    We manage the sold seats here and use the room capacity attribute to determine available seats.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showtime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Showing for {self.movie} in {self.room.name} at {self.showtime}'

    @property
    def sold_seats(self):
        """
        How many tickets have we sold for this showing?
        """
        return self.ticket_set.count()

    def available_seats(self):
        """
        How many seats can still be sold here?
        """
        return self.room.seats_capacity - self.sold_seats

    def seats_available(self, requested=None):
        """
        returns a boolean on whether there are any seats available
        OR
        whether the requested number of seats is available
        """
        if requested:
            return self.available_seats() >= requested
        return self.available_seats() > 0


class Ticket(models.Model):
    """
    Very simple representation of a ticket to a movie showing
    """
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE)

