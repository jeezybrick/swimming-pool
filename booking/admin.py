from django.contrib import admin
from booking.models import Booking

# Register your models here.


class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "swim_lane", "start_date", 'start_time', 'end_time', 'created_at')

admin.site.register(Booking, BookingAdmin)
