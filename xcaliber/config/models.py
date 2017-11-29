from django.db import models
from solo.models import SingletonModel


class WageringRequirement(SingletonModel):
    value = models.IntegerField(default=20)

    def __str__(self):
        return u"Wagering Requirement"

    class Meta:
        verbose_name = "Wagering Requirement"
