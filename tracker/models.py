from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """A topic the user is learning about"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model"""
        return self.text

class Entry(models.Model):
    """Something specific about a topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    blood_sugar = models.IntegerField(blank=True, null=True)
    carbs = models.IntegerField(blank=True, null=True)
    insulin = models.IntegerField(blank=True, null=True)
    BOLUS = 'Fiasp'
    BASAL = 'Tresiba'
    INSULIN_CHOICES = (
        (BASAL, 'Basal'),
        (BOLUS, 'Bolus'),
    )
    insulin_type = models.CharField(max_length=10,
                                    choices=INSULIN_CHOICES,
                                    default=BOLUS,
                                    )
    MANUAL = 'Manual'
    AUTO = 'Dexcom'
    EVENT_CHOICES = (
        (MANUAL, 'Manual'),
        (AUTO, 'Auto'),
    )
    event_type = models.CharField(max_length=10,
                                  choices=EVENT_CHOICES,
                                  default=MANUAL,
                                  )
    date_added = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation of the model."""
        return self.date_added