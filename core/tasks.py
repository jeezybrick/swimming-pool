import datetime
from celery.task import periodic_task
from booking.models import Booking
from my_auth.models import OAuthUser


# periodic task for unblock users with banned date is gone
@periodic_task(run_every=60 * 60)  # run every hour
def unblock_user():
    users = OAuthUser.objects.filter(banned_to__lt=datetime.datetime.now())
    for user in users:
        user.is_auth = True
        user.is_banned = False
        user.banned_to = None
        user.attempt_to_ban = 0
        user.save()


# periodic task for checking if member id is exists in .csv file
@periodic_task(run_every=30)  # run every hour
def check_if_member_id_exist():
    users = OAuthUser.objects.all()
    for user in users:
        user.save()
