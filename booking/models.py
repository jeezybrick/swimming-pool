from django.db import models
from django.conf import settings


class Booking(models.Model):

    user = models.ForeignKey(settings.SOCIAL_AUTH_USER_MODEL, related_name='booking')
    swim_lane = models.SmallIntegerField()
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user
