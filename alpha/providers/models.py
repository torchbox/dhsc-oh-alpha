from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    covers_england = models.BooleanField(null=True)
