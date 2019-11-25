# Cinema 3 - (Extremely Simplified) Example of Microservices in Python


Overview
========

Cinema 3 is an example project which demonstrates the use of microservices for a fictional movie theater. 
The Cinema 3 backend was originally powered by 4 microservices, and currently has 5 services (7 in a neat future). all of which happen to be written in Python using Flask. For more information, you can refer to original blog post here: https://codeahoy.com/2016/07/10/writing-microservices-in-python-using-flask/

 * Movie Service: Provides information like movie ratings, title, etc.
 * Show Times Service: Provides show times information.
 * Booking Service: Provides booking information. 
 * Users Service: Provides movie suggestions for users by communicating with other services.
 * Rewards Service: Provides rewards for uses that have bought various tickets.

Requirements
===========

* Python 3 (Original package was based on python 2.7)
* Works on Linux, Windows, Mac OSX and (quite possibly) BSD.

Install
=======

The quick way is use the provided `make` file.

<code>
$ make install
</code>

Starting and Stopping Services
==============================

To launch the services:

<code>
$ make launch
</code>

To stop the services: 

<code>
$ make shutdown
</code>


APIs and Documentation
======================

## Movie Service (port 5001)

This service is used to get information about a movie. It provides the movie title, rating on a 1-10 scale, 
director and other information.

To lookup all movies in the database, hit: `http://127.0.0.1:5001/movies`


    GET /movies
    Returns a list of all movies.
    
    {
        "267eedb8-0f5d-42d5-8f43-72426b9fb3e6": {
            "director": "Ryan Coogler", 
            "id": "267eedb8-0f5d-42d5-8f43-72426b9fb3e6", 
            "rating": 8.8, 
            "title": "Creed"
    }, 
    ...... output truncated ...... 

To lookup a movie by its `id`:

    GET /movies/7daf7208-be4d-4944-a3ae-c1c2f516f3e6
    Returns the specified movie.
    
    {
        "director": "Paul McGuigan", 
        "id": "7daf7208-be4d-4944-a3ae-c1c2f516f3e6", 
        "rating": 6.4, 
        "title": "Victor Frankenstein", 
        "uri": "/movies/7daf7208-be4d-4944-a3ae-c1c2f516f3e6"
    }
    
## Showtimes Service (port 5002)

This service is used get a list of movies playing on a certain date.

To lookup all showtimes, hit: `http://127.0.0.1:5002/showtimes`


    GET /showtimes
    Returns a list of all showtimes by date.
    
    {
    "20151130": [
        "720d006c-3a57-4b6a-b18f-9b713b073f3c", 
        "a8034f44-aee4-44cf-b32c-74cf452aaaae", 
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab"
    ], 
    ...... output truncated ...... 

To get movies playing on a certain date:

    GET /showtimes/20151201
    Returns all movies playing on the date.

    [
        "267eedb8-0f5d-42d5-8f43-72426b9fb3e6", 
        "7daf7208-be4d-4944-a3ae-c1c2f516f3e6", 
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab", 
        "a8034f44-aee4-44cf-b32c-74cf452aaaae"
    ]

## Booking Service (port 5003)

Used to lookup booking information for users.

To get all bookings by all users in the system, hit: `http://127.0.0.1:5003/bookings`

    GET /bookings
    Returns a list of booking information for all bookings in the database.
    
    {
        "chris_rivers": {
            "20151201": [
                "267eedb8-0f5d-42d5-8f43-72426b9fb3e6"
            ]
        }, 
        ...... output truncated ...... 
    }   
To lookup booking information for a user:

    GET /bookings/dwight_schrute
    
        {
            "20151201": [
                "7daf7208-be4d-4944-a3ae-c1c2f516f3e6", 
                "267eedb8-0f5d-42d5-8f43-72426b9fb3e6"
            ], 
            "20151205": [
                "a8034f44-aee4-44cf-b32c-74cf452aaaae", 
                "276c79ec-a26a-40a6-b3d3-fb242a5947b6"
            ]
        }

To make a new booking the POST request would be:
        
    POST /bookings/new
    {
        "user" : "chris_rivers",
        "date": "20151201"
        "movie": "7daf7208-be4d-4944-a3ae-c1c2f516f3e6"
    }  


## User Service (port 5000)

This service returns information about the users of Cinema 3 and also provides movie suggestions to the 
users. It communicates with other services to retrieve booking or movie information.

To get a list of all the users in the system, hit: `http://127.0.0.1:5000/users`

    GET /users
    Returns a list of all users in the database.
    
    {
        "chris_rivers": {
            "id": "chris_rivers", 
            "last_active": 1360031010, 
            "name": "Chris Rivers"
        }, 
        ...... output truncated ...... 

To lookup information about a user:

    GET /users/michael_scott
    {
        "id": "michael_scott", 
        "last_active": 1360031625, 
        "name": "Michael Scott"
    }
    
To get suggested movies for a user:

    GET /users/michael_scott/suggested

## Rewards Service (port 5004)

This service provides rewards for uses that have bought various tickets.
Everytime a user buy a new ticket his/her scores a new point on the reward service.

To get a list of all the users and their rewards score in the system, hit: `http://127.0.0.1:5000/rewards`

    GET /rewards
    {
        "chris_rivers": {
            "score":1
        },
        "garret_heaton": {
            "score":2
        },
        "dwight_schrute": {
            "score":4
        }
    }

To lookup the score for a user, it goes like this:

    GET /rewards/michael_scott
    {
        "michael_scott": {
            "score":1
            }
    }
