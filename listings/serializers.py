from rest_framework import serializers

from listings.models import BookingInfo


class UnitRequestSerializer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    max_price= serializers.IntegerField()


class UnitResponseSerializer(serializers.ModelSerializer):

    listing_type = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    price = serializers.IntegerField(source="min_price")

    class Meta:
        model = BookingInfo
        fields = ['listing_type', 'title', 'country', 'city', 'price',]

    def get_listing_type(self, obj):
        return obj['listing__listing_type'] or obj['hotel_room_type__hotel__listing_type']

    def get_title(self, obj):
        return obj['listing__title'] or obj['hotel_room_type__hotel__title']

    def get_country(self, obj):
        return obj['listing__country'] or obj['hotel_room_type__hotel__country']

    def get_city(self, obj):
        return obj['listing__city'] or obj['hotel_room_type__hotel__city']