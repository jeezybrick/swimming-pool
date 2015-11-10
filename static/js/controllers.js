/**
 * Created by user on 05.10.15.
 */

angular
    .module('myApp')
    .controller('HomeController', HomeController);

function HomeController($scope, $timeout, AuthUser, Booking, MyBookings, Flash, $auth, $modal) {
    $scope.selectedDate = false;
    $scope.bookingLoad = false;
    $scope.title = 'SignUp';
    $scope.makeOrderModalQuestion = "Do you wan't to make the order?";

    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $scope.user = AuthUser; // Auth user object
    $scope.startPageLoad = false;
    $scope.bookingLoad = false;
    $scope.addOrderMessageSuccess = 'Approved!';
    $scope.selectedDate = moment(date).format('YYYY-MM-DD');

    $scope.delay = $timeout(function () {

        $scope.startPageLoad = true;

    }, 400);

    /* alert on eventClick */
    $scope.alertOnEventClick = function(date, jsEvent, view){

        $scope.alertMessage = (date.format() + ' was clicked ');
        $scope.selectedDate = date.format();
        $scope.test = moment($scope.selectedDate).format('YYYY-MM-DD');

        $scope.booking = Booking.query(params = {date: $scope.selectedDate},function () {

            $scope.bookingLoad = true;

        }, function () {
            $scope.bookingLoadError = true;
        });
    };

    $scope.isUserAuth = function () {
        return $scope.user.id;
    };

    $scope.isUserActive = function () {
        return $scope.user.is_auth;
    };
     /* config object */
    $scope.uiConfig = {
        calendar: {
            height: 450,
            editable: true,
            header: {
                left: '',
                center: 'title',
                right: ''
            },
            dayClick: $scope.alertOnEventClick,
            eventDrop: $scope.alertOnDrop,
            eventResize: $scope.alertOnResize,
            //defaultView: 'basicWeek',
            defaultDate: $scope.test
        }
    };

    $scope.events = [
      {title: 'All Day Event',start: new Date(y, m, 1)},
      {title: 'Long Event',start: new Date(y, m, d - 5),end: new Date(y, m, d - 2)},
      {id: 999,title: 'Repeating Event',start: new Date(y, m, d - 3, 16, 0),allDay: true},
      {id: 999,title: 'Repeating Event',start: new Date(y, m, d + 4, 16, 0),allDay: false},
      {title: 'Birthday Party',start: new Date(y, m, d + 1, 19, 0),end: new Date(y, m, d + 1, 22, 30),allDay: false}
    ];

    /**
     * Get list of bookings for auth user
     */
    if ($scope.isUserAuth() && $scope.isUserActive()) {

        $scope.booking = Booking.query(params = {date: $scope.selectedDate},function () {

            $scope.bookingLoad = true;

        }, function () {
            $scope.bookingLoadError = true;
        });

    }


    /**
     * Add order
     */
    $scope.makeOrder = function (index) {


        $scope.order = new MyBookings();
        $scope.order.start_time =  $scope.booking[index].time_start;
        $scope.order.end_time =  $scope.booking[index].time_end;
        $scope.order.start_date = $scope.selectedDate;

        $scope.order.$save(function (response) {

            $scope.booking[index].is_booked = true;

            // Approved order modal
            var myOtherModal = $modal({
                scope: $scope,
                templateUrl: 'static/partials/modals/approved_order_modal.html',
                show: false,
                placement: 'center',
                animation:'am-fade-and-scale'
            });
            $scope.showModal = function () {
                myOtherModal.$promise.then(myOtherModal.show);
            };
            $scope.delayOnShowApproveModal = $timeout(function () {

                $scope.showModal()

            }, 250);

        }, function (error) {

            $scope.defaultError = error.data;
            $scope.startTimeError = error.data.start_time;
            $scope.startDateError = error.data.start_date;
            Flash.create('danger', $scope.startTimeError || $scope.startDateError || $scope.defaultError, 'flash-message');

        });


    };

    $scope.authenticate = function(provider) {
        $auth.authenticate(provider);
    };
}


angular
    .module('myApp')
    .controller('LoginCtrl', LoginCtrl);

function LoginCtrl($scope, $http, $location,$timeout, $window, Flash, AuthUser) {

    $scope.page = '/api/user/';
    $scope.loginProcess = false;
    $scope.user = AuthUser;
    $scope.title = 'Login';


    $scope.sendLoginData = function () {
        $scope.loginProcess = true;

        $http.post($scope.page, $scope.user).success(function (response) {

            Flash.create('success', response, 'flash-message');
            $scope.delay = $timeout(function () {

                $window.location.href = '/';

            }, 1000);


        }).error(function (error) {

            $scope.sendLoginDataError = error;
            Flash.create('danger', error, 'flash-message');
            $scope.loginProcess = false;
        });
    };



}


angular
    .module('myApp')
    .controller('BookingsController', BookingsController);

function BookingsController($scope, $http, $location, $window, Flash, MyBookings, AuthUser) {

    var date = new Date();
    $scope.currentDate = moment(date).format('MMMM ' + 'YYYY');
    $scope.ordersLoad = false;
    $scope.user = AuthUser;
    $scope.deleteOrderModalQuestion = "Do you wan't to delete this order?";

    $scope.bookings = MyBookings.query(function () {

        $scope.ordersLoad = true;

    }, function () {
        $scope.bookingsLoadError = true;
    });

    $scope.removeOrder = function (index) {


        MyBookings.delete({id: $scope.bookings[index].id}, function () {

            $scope.bookings.splice(index, 1);

        }, function(error){

            $scope.defaultError = error.data;
            $scope.detailError = error.data.detail;
            Flash.create('danger', $scope.detailError || $scope.defaultError, 'flash-message');
        });


    };


}

angular
    .module('myApp')
    .controller('AuthController', AuthController);

function AuthController($scope, AuthUser) {

    $scope.user = AuthUser;
    $scope.title = 'signup';

    if (angular.isDefined($scope.user)) {

        $scope.isUserAuth = function () {
            return $scope.user.id;
        };

        $scope.isUserActive = function () {
            return $scope.user.is_auth;
        };

        if ($scope.isUserAuth() && !$scope.isUserActive()) {
            $scope.title = 'login';
        }

        if (!$scope.isUserAuth() && !$scope.isUserActive()) {
            $scope.title = 'signup';
        }

    }
}

