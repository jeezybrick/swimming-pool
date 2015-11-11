/**
 * Created by user on 05.10.15.
 */

angular
    .module('myApp')
    .controller('HomeController', HomeController);

function HomeController($scope, $timeout, AuthUser, Booking, MyBookings, Flash, $modal, $location) {

    $scope.bookingLoad = false;
    $scope.makeOrderModalQuestion = "Do you wan't to make the order?";
    $scope.selected = 0; // select current day in calendar

    var date = new Date();
    var m = date.getMonth();
    var i;
    $scope.dates = []; // days array for calendar
    $scope.cuntOfDaysInCalendar = 5; // count of days in calendar
    $scope.addOrderMessageSuccess = 'Approved!';
    $scope.dateNow = moment(date).format('MMMM YYYY'); // current date
    $scope.dates.push(moment(date).format('YYYY-MM-DD')); // push current date as first date in calendar

    $scope.selectedDate = moment(date).format('YYYY-MM-DD'); // selected day by user.init-current date

    // function for pushing days for calendar
    for (i = 1; i < $scope.cuntOfDaysInCalendar; i++) {
        $scope.dates.push(moment(date).add(i, 'days').format('YYYY-MM-DD'));
    }

    $scope.user = AuthUser.query(function (response) {

        // if user is not active - redirect
        if (angular.equals(response.is_auth, false)) {
            $location.path('/login/');
        }

        /**
         * Get list of bookings for auth user
         */
        $scope.booking = Booking.query(params = {date: $scope.selectedDate}, function () {

            $scope.bookingLoad = true;

        }, function () {
            $scope.bookingLoadError = true;
        });

    }, function () {

        // if user is not auth
        $location.path('/auth/');

    });


    /**
     * Add order
     */
    $scope.makeOrder = function (index) {


        $scope.order = new MyBookings();
        $scope.order.start_time = $scope.booking[index].time_start;
        $scope.order.end_time = $scope.booking[index].time_end;
        $scope.order.start_date = $scope.selectedDate;

        $scope.order.$save(function (response) {

            $scope.booking[index].is_booked = true;

            // Approved order modal
            var myOtherModal = $modal({
                scope: $scope,
                templateUrl: 'static/partials/modals/approved_order_modal.html',
                show: false,
                placement: 'center',
                animation: 'am-fade-and-scale'
            });
            $scope.showModal = function () {
                myOtherModal.$promise.then(myOtherModal.show);
            };
            $scope.delayOnShowApproveModal = $timeout(function () {

                $scope.showModal()

            }, 250);

        }, function (error) {

            $scope.defaultError = error.data;
            $scope.detailError = error.data.detail;
            $scope.startTimeError = error.data.start_time;
            $scope.startDateError = error.data.start_date;
            Flash.create('danger', $scope.startTimeError || $scope.startDateError || $scope.detailError || $scope.defaultError, 'flash-message');

        });


    };

    /**
     * Sort time for order by date
     */
    $scope.getOrdersBySelectedDate = function (date) {
        $scope.bookingLoad = false;
        $scope.selectedDate = date;

        $scope.booking = Booking.query(params = {date: $scope.selectedDate}, function () {

            $scope.bookingLoad = true;

        }, function () {
            $scope.bookingLoadError = true;
        });
    };

    // active date in calendar on click
    $scope.select = function (index) {
        $scope.selected = index;
    };
}


angular
    .module('myApp')
    .controller('LoginCtrl', LoginCtrl);

function LoginCtrl($scope, $http, $location, $timeout, Flash, AuthUser) {

    $scope.page = '/api/user/';
    $scope.loginProcess = false;
    $scope.title = 'Login';

    $scope.user = AuthUser.query(function (response) {

        if (angular.equals(response.is_auth, false)) {
            //
        } else {
            $location.path('/');
        }

    }, function () {

        $location.path('/');

    });

    // send user's name and mem_id
    $scope.sendLoginData = function () {
        $scope.loginProcess = true;

        $http.post($scope.page, $scope.user).success(function (response) {

            Flash.create('success', response, 'flash-message');
            $scope.delay = $timeout(function () {

                $location.path('/');

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

function BookingsController($scope, $location, Flash, MyBookings, AuthUser) {

    var date = new Date();
    $scope.currentDate = moment(date).format('MMMM ' + 'YYYY');
    $scope.ordersLoad = false;
    $scope.deleteOrderModalQuestion = "Do you wan't to delete this order?";
    $scope.dateNow = moment(date).format('MMMM YYYY');

    $scope.user = AuthUser.query(function (response) {

        if (angular.equals(response.is_auth, false)) {
            $location.path('/login/');
        }

        $scope.bookings = MyBookings.query(function () {

            $scope.ordersLoad = true;

        }, function () {
            $scope.bookingsLoadError = true;
        });


    }, function () {

        $location.path('/');

    });

    //remove order form user's list
    $scope.removeOrder = function (index) {


        MyBookings.delete({id: $scope.bookings[index].id}, function () {

            $scope.bookings.splice(index, 1);

        }, function (error) {

            $scope.defaultError = error.data;
            $scope.detailError = error.data.detail;
            Flash.create('danger', $scope.detailError || $scope.defaultError, 'flash-message');
        });


    };


}

angular
    .module('myApp')
    .controller('AuthController', AuthController);

function AuthController($scope, $location, AuthUser) {

    $scope.title = 'signup';

    $scope.user = AuthUser.query(function (response) {

        if (angular.equals(response.is_auth, false)) {
            $location.path('/login/');
        }

    }, function () {

        $location.path('/auth/');

    });


}