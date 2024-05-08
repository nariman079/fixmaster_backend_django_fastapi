from django.db import models

from src.enums import statuses

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
        choices=statuses.CHOICES_GENDER, 
        default='WOMEN',
        null=True, blank=True
    )
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        verbose_name='Бизнесс'
        )
    service = models.ManyToManyField(
        Service, verbose_name='Услуги'
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

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    telegram_id = models.CharField(
        'Айди Телеграм-аккаунта', 
        max_length=30, 
        null=True, blank=True
        )
    phone = models.CharField(
        'Номер телефона', max_length=30, 
        null=True, blank=True
        )
    username = models.CharField(
        'Имя пользователя', max_length=30, 
        null=True, blank=True
        )

    def __str__(self):
        return self.username

    


