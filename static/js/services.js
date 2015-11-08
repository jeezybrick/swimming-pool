/**
 * Created by user on 05.10.15.
 */


angular.module('myApp.services', ['ngResource'])

    .factory('Booking', function ($resource) {
        return $resource('/api/booking_time/:id/');
    })

    .factory('MyBookings', function ($resource) {
        return $resource('/api/booking/:id/');
    });

