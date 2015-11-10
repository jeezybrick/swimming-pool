from rest_framework import permissions
from booking.models import Booking


# return true if method is safe
def is_safe_method(request):
    if request.method in permissions.SAFE_METHODS:
        return True


# return set of swim lanes
def get_free_swim_lanes(start_time, start_date):
    swim_lanes_default = [1, 2, 3, 4, 5, 6]  # Six swim lanes
    orders = Booking.objects.filter(start_time=start_time, start_date=start_date)  # get booked swim lines
    swim_lanes_on_orders = [order.swim_lane for order in orders]  # get list of booked swim lines
    free_swim_lanes = set(swim_lanes_default) - set(swim_lanes_on_orders)  # get set of free swim lines
    return free_swim_lanes
