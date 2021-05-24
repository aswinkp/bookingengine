from datetime import datetime, timedelta

from django.db.models import Min, Case, When, F, Count, Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView

# Create your views here.
from listings.models import BookingInfo, Reservation, HotelRoom, Listing
from listings.serializers import UnitResponseSerializer, UnitRequestSerializer



def post_or_get(request, key, default=None):
    return request.POST.get(key, request.GET.get(key, default))


class UnitView(generics.ListAPIView):
    serializer_class = UnitResponseSerializer

    def get_queryset(self):
        serializer = UnitRequestSerializer(data=self.request.GET)
        serializer.is_valid()
        validated_data = serializer.validated_data

        check_in = validated_data['check_in']
        check_out = validated_data['check_out']
        max_price = validated_data['max_price']

        """ Implementation details
        Get available rooms and apartments. 
        Calculate booking_info by filtering objects which has available rooms or apartments
        """

        available_rooms = HotelRoom.objects.exclude(reservations__reserved_date__gte=check_in, reservations__reserved_date__lt=check_out)
        available_apartments = Listing.objects.exclude(reservations__reserved_date__gte=check_in, reservations__reserved_date__lt=check_out)

        booking_infos = BookingInfo.objects.filter(Q(hotel_room_type__hotel_rooms__in=available_rooms) | Q(listing__in=available_apartments)).values(
            'listing__title', 'hotel_room_type__hotel__title',
            'listing__listing_type', 'hotel_room_type__hotel__listing_type',
            'listing__country', 'hotel_room_type__hotel__country',
            'listing__city', 'hotel_room_type__hotel__city',
        ).annotate(min_price=Min('price')).filter(min_price__lte=max_price)

        return booking_infos
