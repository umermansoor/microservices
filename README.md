# Microservices with Flask

An example project demonstrating the use of microservices for a hypothetical Movie Theater.

## Overview
Acme Movie theater uses various microservices (all of which happen to be written in Python using Flask) to manage its users and bookings. The four services are:

* Users Service: Provides movie suggestions for users. Runs on port **5000**
 * Movie Service: Movie lookup service. Provides ratings, cast etc. Runs on port **5001**
 * Shows Times Service: Provides show times information. Runs on port **5002**
 * Booking Service: Provides booking information. Runs on port **5003**


## Installation

<code>
$ make install
</code>

## Starting Services
<code>
$ make platform
</code>


