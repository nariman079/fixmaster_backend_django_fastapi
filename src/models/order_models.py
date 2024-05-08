from django.db import models


class Booking(models.Model):
    
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
    master = models.ForeignKey(
        'src.Master', on_delete=models.CASCADE, 
        )

    def __str__(self):
        return str(self.master)


class Order(models.Model):

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
    status = models.CharField(
        'Статус', max_length=20, 
        choices=statuses.CHOICES_STATUS, 
        null=True, blank=True)
    customer = models.ForeignKey(
        'src.Customer', 
        on_delete=models.CASCADE, 
        verbose_name='Клиент'
        )
    master = models.ForeignKey(
        'src.Master', 
        on_delete=models.CASCADE, 
        verbose_name='Мастер'
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

    def __str__(self):
        return str(self.master)