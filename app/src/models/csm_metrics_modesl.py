from django.db import models


class GaugeValue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} = {self.value}"
