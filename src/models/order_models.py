from django.db import models
from src.enums import statuses

class Booking(models.Model):
    """ Брони мастеров """

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирование'

    booking_date = models.DateField(
        'Дата бронирования', 
        null=True, blank=True
        )
    booking_time = models.TimeField(
        'Время бронирования', 
        null=True, blank=True
        )
    booking_end_time = models.TimeField(
        "Длительность процедуры",
        null=True, blank=True, editable=False
    )
    master = models.ForeignKey(
        'src.Master', on_delete=models.CASCADE, 
        )

    def __str__(self):
        return str(self.master)


class Order(models.Model):
    """ Заказы """

    class Meta:

        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    begin_date = models.DateField(
        'Дата начала', 
        null=True, blank=True
        )
    begin_time = models.TimeField(
        'Время начала', 
        null=True, blank=True
        )
    length_time = models.IntegerField(
        "Длительность процедуры",
        null=True, blank=True, editable=False
    )
    status = models.CharField(
        'Статус', max_length=20, 
        choices=statuses.CHOICES_STATUS, 
        default='new',
        null=True, blank=True)
    customer = models.ForeignKey(
        'src.Customer', 
        on_delete=models.CASCADE, 
        verbose_name='Клиент',
        null=True, blank=True
        )
    customer_phone = models.CharField(
        "Номер телефона клиента",
        max_length=30
        )
    payment_id = models.CharField(
        max_length=200,
        null=True, blank=True
        )
    payment_link = models.CharField(
        max_length=500,
        null=True,
        blank=True
        )
    services = models.ManyToManyField(
        'src.Service', 
        null=True, blank=True
        )
    def __str__(self):
        return str(self.customer_phone)