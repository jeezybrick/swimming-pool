import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from my_auth.models import OAuthUser
from booking.models import Booking
from api.utils import get_free_swim_lanes


class UserSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(required=True, max_length=50)
    is_auth = serializers.BooleanField(read_only=True)
    banned_to = serializers.DateTimeField(read_only=True)
    is_banned = serializers.BooleanField(read_only=True)

    class Meta:
        model = OAuthUser
        fields = ('id', 'fullname', 'banned_to', 'is_auth', 'is_banned', )


class BookingSerializer(serializers.ModelSerializer):

    maxDaysToOrder = 86400 * 5  # days selection list limited to the next 5 days
    swim_lane = serializers.IntegerField(read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'swim_lane', 'start_date', 'start_time', 'end_time', )

    def validate_start_date(self, start_date):
        if (start_date - datetime.datetime.now().date()).total_seconds() > self.maxDaysToOrder:
            raise serializers.ValidationError(_("5 days from now is max!"))

        if start_date < datetime.datetime.now().date():
            raise serializers.ValidationError(_("You try order past date"))
        return start_date

    def validate_start_time(self, start_time):
        minutes = start_time.strftime('%M')
        seconds = start_time.strftime('%S')
        interval_in_minutes = '30'  # step in time eg 11:30..12:00

        if not minutes == '00' and not minutes == interval_in_minutes:
            raise serializers.ValidationError(_("Invalid minutes in time"))

        if seconds != '00':
            raise serializers.ValidationError(_("Invalid seconds in time"))

        return start_time
