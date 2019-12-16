# movietheatre

Let's say we have a movie theatre. The movie theatre can have the following things:

        Rooms with a designated capacity (number of seats)
        Movies that are playing at a set time every day
        Tickets that are sold to customers

The API should be able to do the following

        Set up rooms
        Set up movie showtimes
        Sell some tickets

        Look at the list of movie rooms and what they're playing
        Look at the list of movies playing at the theatre
        Buy tickets to a movie


What we're looking for is an API-only implementation of the service, written in Django. 
We are not looking for real payments, nor do we care about separating user roles - the API can be anonymous. 
We would like to see testing, though. 

The endpoints are as follows:
* **/rooms/** 
_list and create rooms_
* **/movies/** 
_list and create movies_
* **/showings/** 
_list and create showings_
* **/showings/< id >** 
_details of a single showing_
* **/showings/< id >/ticket** 
_list and create tickets for a showing_
* **/tickets/< id >** 
_details of a ticket_
