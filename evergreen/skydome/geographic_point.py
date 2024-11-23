import enum
from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class GeographicPoint:
    """A point on Earth in latitude and longitude.
    Positive values for latitude represent North and negative values South.
    Positive values for longitude represent East and negative values West.
    Will raise an Error if an Invalid argument is input.
    Precision will be rounded to that used by the national weather service.
    """

    latitude: float = field(init=True, hash=True, compare=True)
    longitude: float = field(init=True, hash=True, compare=True)

    latitude_degrees_minutes: str = field(init=False, hash=False, compare=False)
    latitude_degrees_minutes_seconds: str = field(init=False, hash=False, compare=False)

    longitude_degrees_minutes: str = field(init=False, hash=False, compare=False)
    longitude_degrees_minutes_seconds: str = field(
        init=False, hash=False, compare=False
    )

    def __validate_latitude(
        self, degrees_latitude: float | int, decimal_precision: int
    ):
        if type(degrees_latitude) is float and type(degrees_latitude) is int:
            raise TypeError()
        if degrees_latitude > 90 or degrees_latitude < -90:
            raise ValueError()
        object.__setattr__(
            self,
            "latitude",
            round(self.latitude, decimal_precision),
        )

    def __validate_longitude(self, degrees_longitude: float, decimal_precision: int):
        if type(degrees_longitude) is float and type(degrees_longitude) is int:
            raise TypeError()
        if degrees_longitude > 180 or degrees_longitude < -180:
            raise ValueError()
        object.__setattr__(
            self,
            "longitude",
            round(self.longitude, decimal_precision),
        )

    def __post_init__(self):
        nat_weather_service_decimal_precision = 4

        self.__validate_latitude(self.latitude, nat_weather_service_decimal_precision)
        self.__validate_longitude(self.longitude, nat_weather_service_decimal_precision)
        self.__set_latitude_strings()
        self.__set_longitude_strings()

    @classmethod
    def _get_degrees(cls, value: int | float) -> int:
        return int(abs(value))

    @classmethod
    def _get_minutes(cls, value: int | float) -> int:
        return int((abs(value) % 1) * 60)

    @classmethod
    def _get_seconds(cls, value: int | float) -> int:
        return int(round((((abs(value) % 1) * 60) % 1) * 60))

    def __set_latitude_strings(self):
        degrees = self._get_degrees(self.latitude)
        minutes = self._get_minutes(self.latitude)
        seconds = self._get_seconds(self.latitude)

        north_south_axis: str = ""
        if self.latitude > 0:
            north_south_axis = " N"
        elif self.latitude < 0:
            north_south_axis = " S"

        degrees = abs(degrees)

        object.__setattr__(
            self,
            "latitude_degrees_minutes",
            f"{degrees}° {minutes}′{north_south_axis}",
        )
        object.__setattr__(
            self,
            "latitude_degrees_minutes_seconds",
            f"{degrees}° {minutes}′ {seconds}″{north_south_axis}",
        )

    def __set_longitude_strings(self):
        degrees = self._get_degrees(self.longitude)
        minutes = self._get_minutes(self.longitude)
        seconds = self._get_seconds(self.longitude)

        east_west_axis: str = ""
        if self.longitude > 0:
            east_west_axis = " E"
        elif self.longitude < 0:
            east_west_axis = " W"

        degrees = abs(degrees)

        object.__setattr__(
            self,
            "longitude_degrees_minutes",
            f"{degrees}° {minutes}′{east_west_axis}",
        )
        object.__setattr__(
            self,
            "longitude_degrees_minutes_seconds",
            f"{degrees}° {minutes}′ {seconds}″{east_west_axis}",
        )


class Locations(GeographicPoint, enum.Enum):
    BONNER_HALL = (43.0015, -78.7880)
    DAVIS_HALL = (43.0024, -78.7876)
    STUDENT_UNION = (43.0014, -78.7859)
    ONE_WORLD = (43.0009, -78.7890)
