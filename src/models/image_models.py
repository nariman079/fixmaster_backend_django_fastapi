"""
Image models in project
"""

from django.db import models


class Image(models.Model):
    """ 
    Изображения
    """

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    image = models.ImageField(
        'Изображение', upload_to='images/'
        )
    priority = models.IntegerField(
        'Приоритет', default=0
        )

    def __str__(self):
        return self.image.name
