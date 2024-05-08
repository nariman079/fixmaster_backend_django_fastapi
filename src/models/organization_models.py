from django.db import models

from .enums import data

class OrganizationType(models.Model):
    """ Типы орзанизаций """

    class Meta:
        verbose_name = "Тип организации"
        verbose_name_plural = "Типы организаций"

    title = models.CharField(
        verbose_name="", max_length=255
        )

class Organization(models.Model):

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

    telegram_id = models.CharField(
        'ID Телеграм', max_length=30, 
        null=True, blank=True
        )
    title = models.CharField(
        'Название', max_length=30, 
        null=True, blank=True
        )
    image = models.ImageField(
        'Изображение', upload_to='business',
        null=True, blank=True
        )
    address = models.CharField(
        'Адрес', max_length=30,
        null=True, blank=True
        )
    contact_phone = models.CharField(
        'Номер телефона', max_length=30, 
        null=True, blank=True
        )
    status = models.BooleanField(
        'Статус', default=True, 
        null=True, blank=True
        )
    time_begin = models.TimeField(
        'Начальное время', 
        null=True, blank=True
        )
    time_end = models.TimeField(
        'Конечное время', 
        null=True, blank=True
        )
    work_schedule = models.CharField(
        'График работы', max_length=30, 
        null=True, blank=True
        )
    type = models.ForeignKey(
        'src.OrganizationType', on_delete=models.PROTECT
        )
    
    def __str__(self):
        return self.title

    


class Master(models.Model):

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    telegram_id = models.CharField(
        'ID Телеграм', max_length=30,
        null=True, blank=True
        )
    name = models.CharField(
        'Имя', max_length=30,
        null=True, blank=True
        )
    surname = models.CharField(
        'Фамилия', max_length=30,
        null=True, blank=True
        )
    image = models.ImageField(
        'Изображние', upload_to='master',
        null=True, blank=True
        )
    gender = models.CharField(
        'Пол', max_length=30,
        choices=data.CHOICES_GENDER, 
        default='WOMEN',
        null=True, blank=True
    )
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        verbose_name='Бизнесс'
        )
    service = models.ManyToManyField(
        Service, verbose_name='Услуги', through=
        )

    def __str__(self):
        return self.name

    


class Image(models.Model):

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    image = models.ImageField(
        'Изображение', upload_to='images/', 
        null=True, blank=True
        )
    priority = models.IntegerField(
        'Приоритет', 
        null=True, blank=True
        )
    
    def __str__(self):
        return self.title






class Service(models.Model):

    class Meta:
        verbose_name = 'Услуги'
        verbose_name_plural = 'Сервисы'

    title = models.CharField(
        'Название', max_length=30,
        null=True, blank=True
        )
    price = models.PositiveIntegerField(
        'Цена', 
        null=True, blank=True
        )
    min_time = models.IntegerField(
        'Минимальное время', 
        null=True, blank=True
        )

    def __str__(self):
        return self.title

    


class Customer(models.Model):
    telegram_id = models.CharField('Айди Телеграм-аккаунта', max_length=30, null=True, blank=True)
    phone = models.CharField('Номер телефона', max_length=30, null=True, blank=True)
    username = models.CharField('Имя пользователя', max_length=30, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Booking(models.Model):
    booking_date = models.DateField('Дата бронирования', null=True, blank=True)
    booking_time = models.TimeField('Время бронирования', null=True, blank=True)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name='Мастер')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирование'

    def __str__(self):
        return str(self.master)


class Order(models.Model):

    begin_date = models.DateField('Дата начала', null=True, blank=True)
    begin_time = models.TimeField('Время начала', null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=data.CHOICES_STATUS, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name='Мастер')

    payment_id = models.CharField(max_length=200, null=True, blank=True)
    payment_link = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return str(self.master)
