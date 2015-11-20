import datetime
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


def get_time_step(request, start_date):

    list = []
    step_in_minutes = 30
    count_of_steps = int(60/step_in_minutes * 24)
    start_step = datetime.datetime.strptime('07:00:00', '%H:%M:%S')
    end_step = datetime.datetime.strptime('07:'+str(step_in_minutes)+':00', '%H:%M:%S')
    temp2 = temp = start_step
    temp4 = temp3 = end_step

    while count_of_steps:

        is_booked = Booking.objects.filter(start_time=temp2, user=request.user, start_date=start_date).exists()
        # return set of free's swim lanes
        free_swim_lanes = get_free_swim_lanes(temp2, start_date)
        if not free_swim_lanes:
            is_booked = True

        list.append({
            'time_start': temp2.strftime('%H:%M:%S'),
            'time_end': temp4.strftime('%H:%M:%S'),
            'is_booked': is_booked,
        })
        # dynamic timestamp
        temp = temp + datetime.timedelta(minutes=step_in_minutes)
        temp3 = temp3 + datetime.timedelta(minutes=step_in_minutes)
        temp2 = temp.time()
        temp4 = temp3.time()
        count_of_steps += -1


    return list
