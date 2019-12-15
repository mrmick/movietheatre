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
        self.assertEqual(str(self.showing),
                         'Showing for %s in %s at %s' % (self.movie.title, self.room.name, self.showing.showtime))

    def test_available_seats_at_start(self):
        self.assertEqual(self.showing.available_seats(), self.showing.room.seats_capacity)

    def test_seats_available_at_start_with_requested_seats(self):
        self.assertTrue(self.showing.seats_available(requested=1))
        self.assertTrue(self.showing.seats_available(requested=50))
        self.assertTrue(self.showing.seats_available(requested=99))
        self.assertTrue(self.showing.seats_available(requested=100))
        # what if we have more than the initial available seats?
        self.assertFalse(self.showing.seats_available(requested=101))

    def test_seats_available_at_start(self):
        self.assertTrue(self.showing.seats_available())

    def test_available_seats_after_selling_some(self):
        self.assertEqual(self.showing.available_seats(), self.showing.room.seats_capacity)
        self.showing.sold_seats = 50
        self.assertEqual(self.showing.available_seats(), self.showing.room.seats_capacity - 50)
        # Make sure we can still see seats as available for purchase
        self.assertTrue(self.showing.seats_available())
        self.assertTrue(self.showing.seats_available(requested=20))
        self.assertTrue(self.showing.seats_available(requested=50))
        self.assertFalse(self.showing.seats_available(requested=51))
