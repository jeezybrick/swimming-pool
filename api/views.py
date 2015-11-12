import csv
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from booking.models import Booking, BookingTimeStep
from api import serializers, utils, validators
from api.permissions import IsAuthorOrReadOnly, IsActiveOrReadOnly
from my_auth.models import OAuthUser


# Standard Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 1


# List of orders
class BookingList(APIView):
    permission_classes = (permissions.IsAuthenticated, IsActiveOrReadOnly, IsActiveOrReadOnly, )

    def get(self, request):
        queryset = Booking.objects.filter(user=self.request.user).order_by('start_date')
        serializer = serializers.BookingSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
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
            return Response('All lines booked at this time:(', status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Order detail
class BookingDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly, IsActiveOrReadOnly)
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
        queryset = BookingTimeStep.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        date = request.GET.get('date', None)

        serializer = serializers.BookingTimeStepSerializer(queryset, context={'request': request,
                                                                              'date': date}, many=True)
        return Response(serializer.data)


# List of orders
class CurrentUserDetail(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        queryset = OAuthUser.objects.get(id=request.user.id)
        serializer = serializers.UserSerializer(queryset, many=False)
        return Response(serializer.data)

    def post(self, request):

        if request.user.is_banned:
            return Response('You banned ;(', status=status.HTTP_403_FORBIDDEN)

        try:
            request.data['mem_id']
        except KeyError:
            return Response('Please, input your member id', status=status.HTTP_400_BAD_REQUEST)

        mem_id = request.data['mem_id']
        # validators.validate_input_member_id(request)
        with open('mem_id.csv') as mem_id_list:
            data = csv.reader(mem_id_list)
            for row in data:
                for fields in row:
                    if str(mem_id) == fields:
                        serializer = serializers.UserSerializer(data=request.data, instance=request.user)
                        if serializer.is_valid():
                            serializer.save(is_auth=True, member_id=mem_id)
                            return Response('You on!', status=status.HTTP_202_ACCEPTED)
                        return Response('Username is required field', status=status.HTTP_400_BAD_REQUEST)

        return Response('Wrong membership card id.', status=status.HTTP_403_FORBIDDEN)
