from django.db import models
import uuid

# Create your models here.


class NationalWeatherServiceAPIInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class HourlyForecast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    datetime = models.DateTimeField()

    last_updated = models.DateTimeField(auto_now_add=True)
    temperature_celsius = models.FloatField()
    dew_point_celsius = models.FloatField()
    relative_humidity_percentage = models.PositiveSmallIntegerField()
    wind_chill_celsius = models.FloatField()
    sky_cover_percentage = models.SmallIntegerField()
    probability_of_precipitation = models.SmallIntegerField()
    quantitative_precipitation_mm = models.FloatField()
