from django.test import TestCase, Client
from theatre.models import Movie, Showing, Room, Ticket
from theatre.serializers import RoomSerializer, MovieSerializer, ShowingSerializer, ShowingDetailSerializer, \
    TicketSerializer, TicketDetailSerializer
from django.utils import timezone
from django.urls import reverse
import json


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
                         'Showing for %s in %s at %s' % (self.movie.title,
                                                         self.room.name,
                                                         format(self.showing.showtime, "%d/%m/%Y, %H:%M")
                                                         )
                         )

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
        for i in range(50):
            Ticket.objects.create(showing=self.showing)
        self.assertEqual(self.showing.sold_seats, 50)
        self.assertEqual(self.showing.available_seats(), self.showing.room.seats_capacity - 50)
        # Make sure we can still see seats as available for purchase
        self.assertTrue(self.showing.seats_available())


class TicketTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Jaba Room", seats_capacity=100)
        self.movie = Movie.objects.create(title="Star Wars")
        self.showing = Showing.objects.create(
            room=self.room,
            movie=self.movie,
            showtime=timezone.now()
        )
        self.ticket = Ticket.objects.create(showing=self.showing)

    def test_str(self):
        self.assertEqual(str(self.ticket),
                         'Ticket #%d sold for Showing for %s in %s at %s' % (self.ticket.pk,
                                                                             self.movie.title,
                                                                             self.room.name,
                                                                             format(self.showing.showtime,
                                                                                    "%d/%m/%Y, %H:%M")
                                                         )
                         )


class RoomListViewTests(TestCase):
    def setUp(self):
        Room.objects.create(name="Jaba Room", seats_capacity=100)
        Room.objects.create(name="Yoda Room", seats_capacity=150)
        Room.objects.create(name="Han Room", seats_capacity=100)

        self.valid_payload = {
            'name': 'Leia Room',
            'seats_capacity': 100
        }
        self.invalid_payload1 = {
            'name': '',
            'seats_capacity': 100
        }
        self.invalid_payload2 = {
            'name': 'Leia Room',
            'seats_capacity': 0
        }

    def test_list_all_rooms(self):
        response = self.client.get(reverse('room_list_create'))
        # make sure we get the appropriate status code
        self.assertEqual(response.status_code, 200)
        # compare against what is in the db
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_room_good_payload(self):
        rooms = Room.objects.all().count()
        # test the positive assertion
        response = self.client.post(reverse('room_list_create'),
                                   data=json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        updated_rooms = Room.objects.all()
        self.assertEqual(rooms + 1, updated_rooms.count())

    def test_create_room_bad_payloads(self):
        # make sure the invalid payloads fail
        for payload in (self.invalid_payload1, self.invalid_payload2):
            response = self.client.post(reverse('room_list_create'),
                                        data=json.dumps(payload),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 400)


class MovieListViewTests(TestCase):
    def setUp(self):
        Movie.objects.create(title="Star Wars: A New Hope")
        Movie.objects.create(title="Star Wars: The Empire Strikes Back")
        Movie.objects.create(title="Star Wars: Return of the Jedi")

        self.valid_payload = {
            'title': 'Solo:  A Star Wars Story'
        }
        self.invalid_payload = {
            'title': ''
        }

    def test_list_all_movies(self):
        response = self.client.get(reverse('movie_list_create'))
        # make sure we get the appropriate status code
        self.assertEqual(response.status_code, 200)
        # compare against what is in the db
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_movie_good_payload(self):
        movies = Movie.objects.all().count()
        # test the positive assertion
        response = self.client.post(reverse('movie_list_create'),
                                   data=json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        updated_movies = Movie.objects.all()
        self.assertEqual(movies + 1, updated_movies.count())

    def test_create_movie_bad_payloads(self):
        # make sure the invalid payloads fail
        response = self.client.post(reverse('movie_list_create'),
                                    data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)


class ShowingListViewTests(TestCase):
    def setUp(self):
        self.room1 = Room.objects.create(name="Jaba Room", seats_capacity=100)
        self.room2 = Room.objects.create(name="Yoda Room", seats_capacity=150)
        self.room3 = Room.objects.create(name="Han Room", seats_capacity=100)
        self.movie1 = Movie.objects.create(title="Star Wars: A New Hope")
        self.movie2 = Movie.objects.create(title="Star Wars: The Empire Strikes Back")
        self.movie3 = Movie.objects.create(title="Star Wars: Return of the Jedi")

        #we really don't care about the time in the tests here, just that it exists
        self.showing1 = Showing.objects.create(room=self.room1, movie=self.movie1, showtime=timezone.now())
        Showing.objects.create(room=self.room2, movie=self.movie2, showtime=timezone.now())
        Showing.objects.create(room=self.room3, movie=self.movie3, showtime=timezone.now())

        self.valid_payload = {
            'room': self.room1.pk,
            'movie': self.movie2.pk,
            'showtime': format(timezone.now(), "%Y-%m-%d %H:%M")
        }
        self.invalid_payload1 = {
            'room': '',
            'movie': 2,
            'showtime': format(timezone.now(), "%d/%m/%Y, %H:%M")
        }
        self.invalid_payload2 = {
            'room': 2,
            'movie': '',
            'showtime': format(timezone.now(), "%d/%m/%Y, %H:%M")
        }
        self.invalid_payload3 = {
            'room': 3,
            'movie': 2,
            'showtime': ''
        }

    def test_list_all_rooms(self):
        response = self.client.get(reverse('showing_list_create'))
        # make sure we get the appropriate status code
        self.assertEqual(response.status_code, 200)
        # compare against what is in the db
        showings = Showing.objects.all()
        serializer = ShowingDetailSerializer(showings, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_showing_good_payload(self):
        showings = Showing.objects.all().count()
        # test the positive assertion
        response = self.client.post(reverse('showing_list_create'),
                                   data=json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        updated_showings = Showing.objects.all()
        self.assertEqual(showings + 1, updated_showings.count())

    def test_create_showing_bad_payloads(self):
        # make sure the invalid payloads fail
        for payload in (self.invalid_payload1, self.invalid_payload2, self.invalid_payload3):
            response = self.client.post(reverse('showing_list_create'),
                                        data=json.dumps(payload),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_detailed_view_loads_single(self):
        response = self.client.get(reverse('showing_detail_update',
                                           kwargs={'pk': self.showing1.pk}))
        # make sure we get the appropriate status code
        self.assertEqual(response.status_code, 200)
        # compare against what is in the db
        serializer = ShowingDetailSerializer(self.showing1)
        self.assertEqual(response.data, serializer.data)


class TicketListViewTests(TestCase):
    def setUp(self):
        self.room1 = Room.objects.create(name="Jaba Room", seats_capacity=100)
        self.room2 = Room.objects.create(name="Yoda Room", seats_capacity=150)
        self.room3 = Room.objects.create(name="Han Room", seats_capacity=100)
        self.movie1 = Movie.objects.create(title="Star Wars: A New Hope")
        self.movie2 = Movie.objects.create(title="Star Wars: The Empire Strikes Back")
        self.movie3 = Movie.objects.create(title="Star Wars: Return of the Jedi")

        #we really don't care about the time in the tests here, just that it exists
        self.showing1 = Showing.objects.create(room=self.room1, movie=self.movie1, showtime=timezone.now())
        self.showing2 = Showing.objects.create(room=self.room2, movie=self.movie2, showtime=timezone.now())
        self.showing3 = Showing.objects.create(room=self.room3, movie=self.movie3, showtime=timezone.now())

        self.ticket1 = Ticket.objects.create(showing=self.showing1)
        Ticket.objects.create(showing=self.showing1)
        Ticket.objects.create(showing=self.showing1)

        self.valid_payload = {
            'showing': self.showing1.pk,
        }
        self.invalid_payload = {
            'showing': '',
        }


    def test_list_all_tickets(self):
        response = self.client.get(reverse('showing_ticket',
                                   kwargs={'pk': self.showing1.pk}))
        # make sure we get the appropriate status code
        self.assertEqual(response.status_code, 200)
        # compare against what is in the db
        tickets = Ticket.objects.all()
        serializer = TicketDetailSerializer(tickets,many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_ticket_good_payload(self):
        tickets = Ticket.objects.filter(showing=self.showing1.pk).count()
        # test the positive assertion
        response = self.client.post(reverse('showing_ticket',
                                            kwargs={'pk': self.showing1.pk}),
                                   data=json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        updated_tickets = Ticket.objects.all()
        self.assertEqual(tickets + 1, updated_tickets.count())

    def test_create_ticket_bad_payloads(self):
        # make sure the invalid payloads fail
        response = self.client.post(reverse('showing_ticket',
                                            kwargs={'pk': self.showing1.pk}),
                                    data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_detailed_view_loads_single(self):
        response = self.client.get(reverse('ticket_detail',
                                           kwargs={'pk': self.ticket1.pk}))
        # make sure we get the appropriate status code
        self.assertEqual(response.status_code, 200)
        # compare against what is in the db
        serializer = TicketDetailSerializer(self.ticket1)
        self.assertEqual(response.data, serializer.data)

