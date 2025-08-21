import smtplib
import logging
import requests

from pathlib import Path
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timezone
from collections import namedtuple

API_ENDPOINT = "http://api.sunrise-sunset.org/json"


# Use namedtuple for location
Location = namedtuple("Location", ["latitude", "longitude"])
berlin = Location(52.51641820726436, 13.377693368816862)

# Define a geographic range around the reference point
RANGE_DELTA = 5.0

# TODO: make this more generic - e.g. with a function get_location_range()
lat_range_my_location = (berlin.latitude - RANGE_DELTA,
                         berlin.latitude + RANGE_DELTA)
lng_range_my_location = (berlin.longitude - RANGE_DELTA,
                         berlin.longitude + RANGE_DELTA)

# TODO: add name of the city
message = """The International Space Station is currently soaring above your location.
If the sky is clear and it's dark enough, step outside
and look up - you might just catch a glimpse of it streaking across the heavens.
It's a rare and awe-inspiring sight, so don't miss the chance to spot humanity's outpost in orbit!"""



def get_iss_position():
    """Fetch the current latitude and longitude of the ISS from the public API."""
    try:
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()
        latitude = float(data["iss_position"]["latitude"])
        longitude = float(data["iss_position"]["longitude"])
        position = (latitude, longitude)
        return position
    except requests.RequestException as e:
        logging.error(f"Error fetching ISS position: {e}")

def get_time() -> datetime:
    """
    Get the current UTC time as a timezone-aware datetime object.

    Returns:
        datetime: Current UTC time.
    """
    return datetime.now(timezone.utc)

def format_time(iso_time_str: str) -> datetime:
    """
    Convert an ISO 8601 datetime string to a timezone-aware datetime object in UTC.

    Args:
        iso_time_str (str): ISO 8601 formatted datetime string (e.g., '2025-08-20T03:56:11+00:00').

    Returns:
        datetime: UTC-aware datetime object.
    """
    return datetime.fromisoformat(iso_time_str).astimezone(timezone.utc)

# TODO: Replace Global Constants with Parameters
#   - easily switch between locations (Berlin, Tokyo, New York e.g.)
#   - support multiple observers or users
#   - make code modular and future-proof
def get_sunrise_sunset(lat: float, lng: float) -> list[datetime] | None:
    """
        Retrieve sunrise and sunset times for a given location.

        Args:
            lat (float): Latitude of the location.
            lng (float): Longitude of the location.

        Returns:
            list[datetime] | None: A list containing sunrise and sunset as UTC datetime objects.
        """
    parameters = {
        "lat": lat,
        "lng": lng,
        "formatted": 0
    }
    try:
        response = requests.get(url=API_ENDPOINT, params=parameters)
        data = response.json()
        sunrise = format_time(data["results"]["sunrise"])
        sunset = format_time(data["results"]["sunset"])
        return [sunrise, sunset]
    except requests.RequestException as e:
        logging.error(f"Error fetching sunrise and sunset times: {e}")

def is_iss_in_range(lat: float, lng: float, lat_range: tuple, lng_range: tuple) -> bool:
    """
        Check whether the ISS is within the defined latitude and longitude range.

        Args:
            lat (float): ISS latitude.
            lng (float): ISS longitude.
            lat_range (tuple): Min and max latitude bounds.
            lng_range (tuple): Min and max longitude bounds.

        Returns:
            bool: True if ISS is within range, False otherwise.
        """
    is_in_lat_range = lat_range[0] <= lat <= lat_range[1]
    is_in_lng_range = lng_range[0] <= lng <= lng_range[1]
    return is_in_lat_range and is_in_lng_range


def send_email(sender: str, password: str, recipient: str, message: str) -> None:
    """
    Send an email notification using Gmail's SMTP server.

    Args:
        sender (str): Sender's email address.
        password (str): App-specific password for authentication.
        recipient (str): Recipient's email address.
        message (str): Email body content.
    """
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(sender, password)
            connection.sendmail(sender, recipient, f"Subject: ISS is flying over\n\n{message}")
        logging.info("Email sent!")
    except smtplib.SMTPException as e:
        logging.error(f"Error sending email: {e}")

def main():
    # TODO: run the code every 60 seconds - add cron job or main_loop()
    env_path = Path(".env")
    load_dotenv(dotenv_path=env_path)
    logging.basicConfig(level=logging.INFO)

    env_vars = dotenv_values(env_path)
    email = env_vars.get("EMAIL")
    app_password = env_vars.get("APP_PASSWORD")
    send_to = env_vars.get("SEND_TO")

    sunrise, sunset = get_sunrise_sunset(berlin.latitude, berlin.longitude)
    current_time = get_time()
    is_dark = sunset < current_time < sunrise

    latitude, longitude = get_iss_position()
    is_flying_over = is_iss_in_range(latitude, longitude, lat_range_my_location, lng_range_my_location)

    if is_dark and is_flying_over:
        send_email(message=message, sender=email, password=app_password, recipient=send_to)
    else:
        logging.info("No notification sent.")

if __name__ == '__main__':
    main()


