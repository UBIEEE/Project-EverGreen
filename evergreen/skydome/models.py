from django.db import models
import uuid

# Create your models here.


# TODO: Generalize these models so that they could work with any API in the future.
class NationalWeatherServiceAPIInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class HourlyForecast(models.Model):
    # metadata fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    datetime_utc = models.DateTimeField()  # Stored in Coordinated Universal Time
    last_updated_utc = models.DateTimeField(
        auto_now_add=True
    )  # Stored in Coordinated Universal Time

    # data fields
    temperature_celsius = models.FloatField()
    dew_point_celsius = models.FloatField()
    relative_humidity_percentage = models.PositiveSmallIntegerField()
    wind_chill_celsius = models.FloatField()
    sky_cover_percentage = models.SmallIntegerField()
    probability_of_precipitation = models.SmallIntegerField()
    quantitative_precipitation_mm = models.FloatField()
