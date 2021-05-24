from django.db import models


class Listing(models.Model):
    HOTEL = 'hotel'
    APARTMENT = 'apartment'
    LISTING_TYPE_CHOICES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
    )

    listing_type = models.CharField(
        max_length=16,
        choices=LISTING_TYPE_CHOICES,
        default=APARTMENT
    )
    title = models.CharField(max_length=255,)
    country = models.CharField(max_length=255,)
    city = models.CharField(max_length=255,)

    def __str__(self):
        return self.title
    

class HotelRoomType(models.Model):
    hotel = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_room_types'
    )
    title = models.CharField(max_length=255,)

    def __str__(self):
        return f'{self.hotel} - {self.title}'


class HotelRoom(models.Model):
    hotel_room_type = models.ForeignKey(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_rooms'
    )
    room_number = models.CharField(max_length=255,)

    def __str__(self):
        return f'{self.room_number} - {self.hotel_room_type}'


class   BookingInfo(models.Model):
    listing = models.OneToOneField(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info'
    )
    hotel_room_type = models.OneToOneField(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info',
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        if self.listing:
            obj = self.listing
        else:
            obj = self.hotel_room_type
            
        return f'{obj} {self.price}'


class Reservation(models.Model):
    listing = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    hotel_room = models.ForeignKey(
        HotelRoom,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    reserved_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        # unique constraint to the reservations in database level
        constraints = [
            models.UniqueConstraint(fields=['hotel_room', 'reserved_date'], name="uniq_room_rsv"),
            models.UniqueConstraint(fields=['listing', 'reserved_date'], name="uniq_apartment_rsv"),
        ]

    def __str__(self) -> str:
        if self.listing:
            return f'{self.listing.__str__()} | {self.reserved_date}'
        else:
            return f'{self.hotel_room.hotel_room_type.__str__()} | {self.reserved_date}'