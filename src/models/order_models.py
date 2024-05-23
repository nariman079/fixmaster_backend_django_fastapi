from django.db import models
from src.enums import statuses


class Booking(models.Model):
    """ Брони мастеров """

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирование'

    booking_date = models.DateField(
        'Дата бронирования', 
        )
    booking_time = models.TimeField(
        'Время бронирования', 
        )
    booking_end_time = models.TimeField(
        "Длительность процедуры",
        editable=False
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
        )
    begin_time = models.TimeField(
        'Время начала', 
        )
    length_time = models.IntegerField(
        "Длительность процедуры",
        null=True, blank=True, editable=False
    )
    status = models.CharField(
        'Статус', max_length=20, 
        choices=statuses.CHOICES_STATUS, 
        default='new'
    )
    customer = models.ForeignKey(
        'src.Customer', 
        on_delete=models.SET_NULL,
        verbose_name='Клиент',
        null=True, blank=True
    )
    customer_phone = models.CharField(
        "Номер телефона клиента",
        max_length=30
    )
    customer_name = models.CharField(
        "Имя клиента",
        max_length=60
    )
    customer_notice = models.CharField(
        "Коментарий",
        max_length=120,
        null=True, blank=True
    )
    payment_id = models.CharField(
        max_length=200,
        default=' '
        )
    payment_link = models.CharField(
        max_length=500,
        default=' '
        )
    services = models.ManyToManyField(
        'src.Service', 
        null=True, blank=True
        )

    def __str__(self):
        return str(self.customer_phone)
