"""Models for the Points Database"""

from django.db import models

# Create your models here.

class Event(models.Model):
    """Table to record the name of different events at a tournament"""
    event_name = models.CharField(max_length=200, unique=False)
    tournament_name = models.CharField(max_length=32, unique=False)
    event_id = models.CharField(max_length=32, primary_key=True)
    event_season = models.CharField(max_length=32, unique=False)
    event_date = models.DateField()


class Fencer(models.Model):
    """Table to record Fencer names"""
    given_name = models.CharField(max_length=200, unique=False)
    family_name = models.CharField(max_length=200, unique=False)
    fencer_id = models.CharField(max_length=200, primary_key=True)


class Points(models.Model):
    """Table to record the number of points earned by each fencer at each event"""
    competitor_id = models.ForeignKey(Fencer, on_delete=models.CASCADE)
    event_placed = models.ForeignKey(Event, on_delete=models.CASCADE)
    points = models.IntegerField()
