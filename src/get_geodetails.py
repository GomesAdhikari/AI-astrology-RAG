from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime

def get_location_details(city: str, country: str) -> dict:
    """
    Fetches the latitude, longitude, and timezone offset for the given city and country.
    """
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(f"{city}, {country}")

    if not location:
        raise ValueError("Invalid city or country. Please check the inputs.")

    latitude = location.latitude
    longitude = location.longitude

    tz_finder = TimezoneFinder()
    timezone_name = tz_finder.timezone_at(lat=latitude, lng=longitude)

    if not timezone_name:
        raise ValueError("Could not determine the timezone for the given location.")

    timezone = pytz.timezone(timezone_name)
    offset = datetime.now(timezone).utcoffset().total_seconds() / 3600

    return {
        'latitude': latitude,
        'longitude': longitude,
        'timezone': offset
    }
