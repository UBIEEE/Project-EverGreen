from geographic_point import GeographicPoint, Locations
import requests
import json
from typing import NamedTuple
import datetime

# TODO: Re-implement this module once a task scheduler is added to the project.


# Using NamedTuple over dataclass because this is already hacky anyway and I want performance on these API
# calls do that the unlikely soul that doesn't hit the cached version won't have their browser yell at them
# for too slow of a response time
class NationalWeatherServiceAPIFinalEndpoints(NamedTuple):
    forecast_office: str
    weekly_forecast: str
    hourly_forecast: str
    grid_data: str
    observation_stations: str

    last_updated_utc: datetime.datetime


def generate_water_state_graph(): ...


def get_grid_point_data_from_national_weather_service(
    geographic_location: GeographicPoint,
): ...


def __get_final_national_weather_api_endpoints(
    geographic_location: GeographicPoint,
) -> NationalWeatherServiceAPIFinalEndpoints:
    unparsed_information: dict = __get_national_weather_api_point_initial_endpoint(
        geographic_location
    )

    properties_table = unparsed_information["properties"]

    forecast_office_endpoint = properties_table["forecastOffice"]
    weekly_forecast_endpoint = properties_table["forecast"]
    hourly_forecast_endpoint = properties_table["forecastHourly"]
    grid_data_endpoint = properties_table["forecastGridData"]
    observation_stations_for_location_endpoint = properties_table["observationStations"]

    current_time: datetime.datetime = datetime.datetime.now().astimezone(
        datetime.timezone.utc
    )

    endpoints = NationalWeatherServiceAPIFinalEndpoints(
        forecast_office_endpoint,
        weekly_forecast_endpoint,
        hourly_forecast_endpoint,
        grid_data_endpoint,
        observation_stations_for_location_endpoint,
        current_time,
    )
    return endpoints


def __get_national_weather_api_point_initial_endpoint(
    geographic_location: GeographicPoint,
):
    url = f"https://api.weather.gov/points/{geographic_location.latitude},{geographic_location.longitude}"

    ub_ieee_email: str = "ubuffalo.ieee@gmail.com"
    headers = {"User-Agent": ub_ieee_email}

    response: requests.Response = requests.get(url=url, headers=headers)

    unparsed_information: dict = json.loads(response.content)
    return unparsed_information


def update_db_with_hourly_forecast_data():
    # get the current link grid point link for our location, either it is cached or will need to re-send

    # make a request to the grid point link

    # parse the data out from that grid point link

    # determine tables of information to update for each hour that we have been given

    # update the database with the new information

    ...
