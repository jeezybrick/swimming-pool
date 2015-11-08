from django.core.mail import send_mail
from rest_framework import generics, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from booking.models import Booking, BookingTimeStep
from api import serializers
from api.permissions import IsAuthorOrReadOnly
from my_auth.models import OAuthUser


# Standard Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 1


# List of orders
class BookingList(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        queryset = Booking.objects.filter(user=self.request.user).order_by('start_date')
        serializer = serializers.BookingSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Order detail
class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)


# List of time.30 min step
class BookingTimeStepList(generics.GenericAPIView):
    serializer_class = serializers.BookingTimeStepSerializer
    queryset = BookingTimeStep.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

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
        serializer = serializers.UserSerializer(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save(is_auth=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
