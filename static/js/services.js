/**
 * Created by user on 05.10.15.
 */


angular.module('myApp.services', ['ngResource'])

    .factory('Booking', function ($resource) {
        return $resource('/api/booking_time/:id/'
        , {id: '@id'}, {
            'query': {method: 'GET', isArray: true}
        });
    })

    .factory('MyBookings', function ($resource) {
        return $resource('/api/booking/:id/');
    })
    .factory('AuthUser', function ($resource) {
        return $resource('/api/user/:id/'
        , {id: '@id'}, {
            'update': {method: 'PUT'},
            'get': {method: 'GET'},
            'query': {method: 'GET', isArray: false}
        });
    });

