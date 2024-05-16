from django.db import models

from src.enums import statuses


class OrganizationType(models.Model):
    """ Типы орзанизаций """

    class Meta:
        verbose_name = "Тип организации"
        verbose_name_plural = "Типы организаций"

    title = models.CharField(
        verbose_name="Типы оргинизаций", max_length=255
        )


class Organization(models.Model):
    """
    Модель организаций.
    """
    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

    telegram_id = models.CharField(
        'ID Телеграм', max_length=30,
        editable=False
        )
    title = models.CharField(
        'Название', max_length=30, 
        )
    image = models.ImageField(
        'Заглавное изображение', upload_to='business',
        )
    address = models.CharField(
        'Адрес', max_length=30,
        )
    contact_phone = models.CharField(
        'Номер телефона', max_length=30, 
        )
    time_begin = models.TimeField(
        'Начало рабочего дня', 
        )
    time_end = models.TimeField(
        'Конец рабочего дня', 
        )
    work_schedule = models.CharField(
        'График работы', max_length=30
        )
    organization_type = models.ForeignKey(
        'src.OrganizationType', on_delete=models.PROTECT
        )
    gallery = models.ManyToManyField(
        'src.Image'
    )
    
    def __str__(self):
        return self.title


class Master(models.Model):
    """
    Модель мастеров
    """
    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    telegram_id = models.CharField(
        'ID Телеграм', max_length=30,
        default="web_user",
        editable=False
        )
    name = models.CharField(
        'Имя', max_length=30,
        )
    surname = models.CharField(
        'Фамилия', max_length=30,
        )
    image = models.ImageField(
        'Изображние', upload_to='master',

        )
    gender = models.CharField(
        'Пол', max_length=30,
        choices=statuses.CHOICES_GENDER,
        default='MEN',
        null=True, blank=True
    )
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        verbose_name='Организация'
        )

    def __str__(self):
        return self.name


class Service(models.Model):
    """
    Модель услуг мастеров
    """
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
    master = models.ForeignKey(
        'src.Master', on_delete=models.CASCADE,
        null=True, blank=True
    )
    title = models.CharField(
        'Название', max_length=30,
        null=True, blank=True
        )
    price = models.PositiveIntegerField(
        'Стоимость', 
        null=True, blank=True
        )
    min_time = models.IntegerField(
        'Минимальная длительность процедуры', 
        null=True, blank=True
        )

    def __str__(self):
        return self.title


class Customer(models.Model):
    """
    Модель клиентов
    """
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    telegram_id = models.CharField(
        'ID Телеграм', 
        max_length=30, editable=False
        
        )
    phone = models.CharField(
        'Номер телефона', max_length=30, 
        null=True, blank=True
        )
    username = models.CharField(
        'Имя пользователя', max_length=30, 
        null=True, blank=True
        )
    addidional_info = models.CharField(
        "Дополнительная информация",
        max_length=255, null=True, blank=True
    )
    
    def __str__(self):
        return self.username

    