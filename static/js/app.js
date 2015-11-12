/**
 * Created by user on 05.10.15.
 */

angular
    .module('myApp', [
        'ngRoute',
        'ui.router',
        'ui.calendar',
        'ui.bootstrap',
        'ngAnimate',
        'ngResource',
        'ngSanitize',
        'myApp.services',
        'flash',
        'mgcrea.ngStrap',
        'ngMaterial',
        'angular-loading-bar',
        'angular.filter',
        'ngMessages'

    ])
    .config(function ($locationProvider, $httpProvider, $resourceProvider, $interpolateProvider, $routeProvider,
                      $compileProvider, $stateProvider, $urlRouterProvider) {

        // CSRF Support
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $resourceProvider.defaults.stripTrailingSlashes = false;

        // Force angular to use square brackets for template tag
        // The alternative is using {% verbatim %}
        $interpolateProvider.startSymbol('[[').endSymbol(']]');

        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension):/);

        // enable html5Mode for pushstate ('#'-less URLs)
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');


        // Routing
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('auth', {
                url: '/auth/',
                templateUrl: '/static/partials/my_auth/auth.html',
                controller: 'AuthController'
            })
            .state('auth-login', {
                url: '/login/',
                templateUrl: '/static/partials/my_auth/login.html',
                controller: 'LoginCtrl'
            })
            .state('home', {
                url: '/',
                templateUrl: '/static/partials/home.html',
                controller: 'HomeController'
            })
            .state('my-bookings', {
                url: '/my_bookings/',
                templateUrl: '/static/partials/my-bookings.html',
                controller: 'BookingsController'
            })
            .state('otherwise', {
                url : '*path',
                templateUrl: '/static/partials/home.html',
                controller: 'HomeController'
            })

    });