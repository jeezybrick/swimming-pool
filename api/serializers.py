import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from my_auth.models import OAuthUser
from booking.models import Booking, BookingTimeStep


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = OAuthUser
        fields = ('fullname', )

    def validate(self, value):
        print(value)
        return value


class BookingSerializer(serializers.ModelSerializer):

    maxDaysToOrder = 86400 * 5  # 5 days

    class Meta:
        model = Booking
        fields = ('id', 'swim_lane', 'start_date', 'start_time', 'end_time', )

    def validate_start_date(self, start_date):
        if (start_date - datetime.datetime.now().date()).total_seconds() > self.maxDaysToOrder:
            raise serializers.ValidationError(_("Error!"))
        return start_date


class BookingTimeStepSerializer(serializers.ModelSerializer):

    is_booked = serializers.SerializerMethodField(read_only=True)

    def get_is_booked(self, obj):
        request = self.context.get('request', None)
        date = self.context.get('date', None)
        return Booking.objects.filter(start_time=obj.time_start, user=request.user, start_date=date).exists()

    class Meta:
        model = BookingTimeStep
        fields = ('id', 'time_start', 'time_end', 'is_booked', )
