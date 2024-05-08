from .models import organization_models


def create_booking(sender, created, instance, **kwargs):
    if created:
        organization_models.Booking.objects.create(booking_date=instance.begin_date, booking_time=instance.begin_time,
                                      master=instance.master)
