from django.contrib import admin
from theatre.models import Room, Movie, Showing, Ticket

# Register your models here.
admin.site.register(Room)
admin.site.register(Movie)
admin.site.register(Showing)
admin.site.register(Ticket)
