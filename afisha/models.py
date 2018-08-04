from django.db import models


class Bitcoin(models.Model):
    """Биток"""
    total = models.CharField("Тотал", max_length=50)
    blocks = models.IntegerField("Blocks", default=0)

    def __str__(self):
        return self.total
