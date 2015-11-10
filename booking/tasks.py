

import datetime
from celery.task import periodic_task
from booking.models import Booking


@periodic_task(run_every=30)
def test_action():
    print('allalala')
