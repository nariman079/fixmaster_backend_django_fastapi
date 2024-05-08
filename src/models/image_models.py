from django.db import models


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
