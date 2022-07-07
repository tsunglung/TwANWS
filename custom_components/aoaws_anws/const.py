"""Constants for ANWS AOAWS Integration."""
from datetime import timedelta
from homeassistant.const import (
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    LENGTH_KILOMETERS,
    PERCENTAGE,
    SPEED_MILES_PER_HOUR,
    TEMP_CELSIUS,
    UV_INDEX,
)
from homeassistant.components.weather import (
    ATTR_CONDITION_CLOUDY,
    ATTR_CONDITION_EXCEPTIONAL,
    ATTR_CONDITION_FOG,
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_LIGHTNING,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_CONDITION_POURING,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_SUNNY,
    ATTR_CONDITION_WINDY,
    ATTR_CONDITION_WINDY_VARIANT,
)

DOMAIN = "aoaws_anws"

DEFAULT_NAME = "ANWS AOAWS"
DEFAULT_LANGUAGE = "tw"
ATTRIBUTION = "Data provided by the Taiwan Air Navigation & Weather Services"
ATTR_LAST_UPDATE = "last_update"
ATTR_SENSOR_ID = "sensor_id"
ATTR_SITE_ID = "site_id"
ATTR_SITE_NAME = "site_name"
ATTR_WEATHER_TEXT = "weather"
CONF_LANGUAGE = "language"
CONF_LOCATION_NAME = "location_name"
CONFIG_FLOW_VERSION = 1
UPDATE_LISTENER = "update_listener"
PLATFORMS = ["sensor", "weather"]

DEFAULT_SCAN_INTERVAL = timedelta(minutes=15)

ANWS_AOAWS_DATA = "anws_aoaws_data"
ANWS_AOAWS_COORDINATOR = "anws_aoaws_coordinator"
ANWS_AOAWS_MONITORED_CONDITIONS = "anws_aoaws_monitored_conditions"
ANWS_AOAWS_NAME = "anws_aoaws_name"

USER_AGENT = ""
HA_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
    "(KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 OPR/38.0.2220.41"
BASE_URL = 'https://aoaws.anws.gov.tw/AWS/mainRight.php?lang={}&voice_alarm=0&state=Taiwan'

REQUEST_TIMEOUT = 10  # seconds

SITES = [
    "Taoyuan",
    "Taipei",
    "Kaohsiung",
    "Taitung",
    "Hengchun",
    "Kinmen",
    "Beigan",
    "Nangan",
    "Ludao",
    "Lanyu",
    "Penghu",
    "Qimei",
    "Wang-an",
    "Taichung",
    "Chaiyi",
    "Tainan",
    "Hualien"
]

LANGUAGES = [
    "en",
    "tw",
]

CONDITION_CLASSES = {
    ATTR_CONDITION_EXCEPTIONAL: [
        "tornado",
        "hurricane conditions",
        "tropical storm conditions",
        "dust",
        "smoke",
        "haze",
        "hot",
        "cold",
    ],
    ATTR_CONDITION_SNOWY: [
        "snow",
        "sleet",
        "snow/sleet",
        "blizzard",
        "light snow",
        "light snow shower",
        "heavy snow",
        "heavy snow shower"
    ],
    ATTR_CONDITION_SNOWY_RAINY: [
        "rain/snow",
        "rain/sleet",
        "freezing rain/snow",
        "freezing rain",
        "rain/freezing rain",
    ],
    ATTR_CONDITION_HAIL: [
        "hail",
        "hail shower"
    ],
    ATTR_CONDITION_LIGHTNING_RAINY: [
        "thunder shower",
        "thunderstorm (high cloud cover)",
        "thunderstorm (medium cloud cover)",
        "thunderstorm (low cloud cover)",
    ],
    ATTR_CONDITION_LIGHTNING: [
        "thunder"
    ],
    ATTR_CONDITION_POURING: [
        "heavy rain shower",
        "heavy rain"
    ],
    ATTR_CONDITION_RAINY: [
        "rain",
        "rain showers (high cloud cover)",
        "rain showers (low cloud cover)",
        "vcts",
        "vcsh",
        "vcts vcsh"
    ],
    ATTR_CONDITION_WINDY_VARIANT: [
        "mostly cloudy and windy",
        "overcast and windy"
    ],
    ATTR_CONDITION_WINDY: [
        "fair/clear and windy",
        "a few clouds and windy",
        "partly cloudy and windy",
    ],
    ATTR_CONDITION_FOG: [
        "fog",
        "mist",
        "fog/mist"
    ],
    "clear": [
        "clear",
        "fair",
        "fair/clear"
    ],  # sunny and clear-night
    ATTR_CONDITION_CLOUDY: [
        "mostly cloudy",
        "overcast"
    ],
    ATTR_CONDITION_PARTLYCLOUDY: [
        "a few clouds",
        "partly cloudy"
    ],
}

VISIBILITY_CLASSES = {
    "Very Poor": 0.1,
    "Poor": 0.4,
    "Moderate": 1,
    "Good": 2,
    "Very Good": 4,
    "Excellent": 8,
    "Extreme Excellent": 10
}

# Sensor types are defined as:
#   variable -> [0]title, [1]device_class, [2]units, [3]icon, [4]enabled_by_default
SENSOR_TYPES = {
    # "name": ["Station Name", None, None, "mdi:label-outline", False],
    "weather": [
        "Weather",
        None,
        None,
        "mdi:weather-sunny",  # but will adapt to current conditions
        True,
    ],
    "temperature": ["Temperature", DEVICE_CLASS_TEMPERATURE, TEMP_CELSIUS, None, True],
    "wind_speed": [
        "Wind Speed",
        None,
        "knot",
        "mdi:weather-windy",
        True,
    ],
    "wind_direction": ["Wind Direction", None, None, "mdi:compass-outline", True],
    # "wind_gust": ["Wind Gust", None, SPEED_MILES_PER_HOUR, "mdi:weather-windy", False],
    "visibility": ["Visibility", None, None, "mdi:eye", True],
    "visibility_distance": [
        "Visibility Distance",
        None,
        LENGTH_KILOMETERS,
        "mdi:eye",
        True,
    ],
    # "uv": ["UV Index", None, UV_INDEX, "mdi:weather-sunny-alert", False],
    # "precipitation": [
    #     "Probability of Precipitation",
    #     None,
    #     PERCENTAGE,
    #     "mdi:weather-rainy",
    #     False,
    # ],
    # "humidity": ["Humidity", DEVICE_CLASS_HUMIDITY, PERCENTAGE, None, False],
}
