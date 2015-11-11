import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from my_auth.models import OAuthUser
from booking.models import Booking, BookingTimeStep
from api.utils import get_free_swim_lanes


class UserSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(required=True, max_length=50)

    class Meta:
        model = OAuthUser
        fields = ('fullname', )


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


class BookingTimeStepSerializer(serializers.ModelSerializer):

    is_booked = serializers.SerializerMethodField(read_only=True)

    def get_is_booked(self, obj):
        request = self.context.get('request', None)
        start_time = obj.time_start
        start_date = self.context.get('date', None)

        # return set of free's swim lanes
        free_swim_lanes = get_free_swim_lanes(start_time, start_date)
        if not free_swim_lanes:
            return True

        return Booking.objects.filter(start_time=obj.time_start, user=request.user, start_date=start_date).exists()

    class Meta:
        model = BookingTimeStep
        fields = ('id', 'time_start', 'time_end', 'is_booked', )
