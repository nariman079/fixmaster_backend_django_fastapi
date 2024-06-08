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
    organization = models.ForeignKey(
        'src.Organization',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        'Изображение', upload_to='images/',
        null=True, blank=True
        )
    image_url = models.CharField(
        max_length=700,
        null=True, blank=True
    )
    priority = models.IntegerField(
        'Приоритет', default=0
        )

    def __str__(self):
        return self.image.name
