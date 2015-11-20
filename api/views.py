import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from booking.models import Booking, BookingTimeStep
from api import serializers, utils, validators
from api.permissions import IsAuthorOrReadOnly, IsActive
from my_auth.models import OAuthUser


# Standard Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 1


# List of orders
class BookingList(APIView):
    permission_classes = (permissions.IsAuthenticated, IsActive, IsActive, )

    def get(self, request):
        queryset = Booking.objects.filter(user=self.request.user).order_by('start_date')
        serializer = serializers.BookingSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        no_free_swim_lanes_text = _('All lines booked at this time:(')

        serializer = serializers.BookingSerializer(data=request.data)
        if serializer.is_valid():

            # return set of free's swim lanes
            free_swim_lanes = utils.get_free_swim_lanes(request.data['start_time'], request.data['start_date'])

            # Save order if free line exists at this time
            if free_swim_lanes:
                serializer.save(user=self.request.user, swim_lane=min(free_swim_lanes))
                '''
                send_mail('Subject here', 'Here is the message.', 'smooker14@gmail.com', ['smooker14@gmail.com'],
                          fail_silently=False)
                '''
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(no_free_swim_lanes_text, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Order detail
class BookingDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly, IsActive)
    maxTime = 5 * 60  # 5 minutes grace period
    maxRemoveAttempt = 3
    bannedToDays = 5

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = serializers.BookingSerializer(order)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        if (timezone.now() - order.created_at).total_seconds() >= self.maxTime:
            user = OAuthUser.objects.get(id=request.user.id)
            user.attempt_to_ban += 1

            if user.attempt_to_ban >= self.maxRemoveAttempt:
                user.is_auth = False
                user.is_banned = True
                user.banned_to = timezone.now() + timezone.timedelta(days=self.bannedToDays)
            user.save()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# List of time.30 min step
class BookingTimeStepList(generics.GenericAPIView):
    serializer_class = serializers.BookingTimeStepSerializer
    queryset = BookingTimeStep.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):

        date = request.GET.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
        list = utils.get_time_step(request, date)

        return Response(list)


# Current user detail
class CurrentUserDetail(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        queryset = OAuthUser.objects.get(id=request.user.id)
        serializer = serializers.UserSerializer(queryset, many=False)
        return Response(serializer.data)

    def post(self, request):

        ban_text = _('You have been banned ;(')

        if request.user.is_banned:
            return Response(ban_text, status=status.HTTP_403_FORBIDDEN)

        return validators.validate_input_member_id(request)