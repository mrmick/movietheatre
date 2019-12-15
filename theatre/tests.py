from django.test import TestCase
from theatre.models import Movie, Showing, Room
from django.utils import timezone


# Create your tests here.
class RoomTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Jaba Room", seats_capacity=100)

    def test_str(self):
        self.assertEqual(str(self.room), 'Jaba Room (100 seats)')

    def test_room(self):
        self.assertIsInstance(self.room, Room)
        self.assertEqual(self.room.name, 'Jaba Room')
        self.assertEqual(self.room.seats_capacity, 100)


class MovieTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title="Star Wars")

    def test_str(self):
        self.assertEqual(str(self.movie), self.movie.title)

    def test_movie(self):
        self.assertIsInstance(self.movie, Movie)
        self.assertEqual(self.movie.title, 'Star Wars')

class ShowingTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Jaba Room", seats_capacity=100)
        self.movie = Movie.objects.create(title="Star Wars")
        self.showing = Showing.objects.create(
            room=self.room,
            movie=self.movie,
            showtime=timezone.now()
        )

    def test_str(self):
        self.assertEqual(str(self.showing), 'Showing for %s in %s at %s' % (self.movie.title, self.room.name, self.showing.showtime))
