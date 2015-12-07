# Cinema 3 - (Extremely Simplified) Example of Microservices in Python


Overview
========

Cinema 3 is an example project which demonstrates the use of microservices for a fictional movie theater. 
The Cinema 3 backend is powered by 4 microservices, all of which happen to be written in Python using 
Flask.

 * Movie Service: Provides information like movie ratings, title, etc.
 * Show Times Service: Provides show times information.
 * Booking Service: Provides booking information. 
 * Users Service: Provides movie suggestions for users by communicating with other services.

Requirements
===========

* Python 2.7
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
