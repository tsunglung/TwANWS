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

WEATHER_CODES = {
    "Clear": "0",
    "Sunny": "1",
    "Partly Cloudy": "3",
    "Mostly Cloudy": "4",
    "Mist": "5",
    "Fog": "6",
    "Cloudy": "7",
    "Overcast": "8",
    "Mist ": "8",
    "VCTS Mist": "9",
    "VCTS VCSH ": "9",
    "Shower Mist": "10",
    "Drizzle": "11",
    "Rain": "12",
    "Heavy rain shower": "13",
    "Heavy rain shower ": "14",
    "Heavy rain": "15",
    "Sleet shower": "16",
    "Sleet shower ": "17",
    "Sleet": "18",
    "Hail shower": "19",
    "Hail shower ": "20",
    "Hail": "21",
    "Shower": "22",
    "Light snow shower": "23",
    "Light snow": "23",
    "Heavy snow shower": "25",
    "Heavy snow shower ": "26",
    "Heavy snow": "27",
    "Thunder shower": "28",
    "Thunder shower ": "29",
    "Thunder": "30"
}

CONDITION_CLASSES = {
    ATTR_CONDITION_CLOUDY: ["3", "4"],
    ATTR_CONDITION_FOG: ["5", "6"],
    ATTR_CONDITION_HAIL: ["19", "20", "21"],
    ATTR_CONDITION_LIGHTNING: ["30"],
    ATTR_CONDITION_LIGHTNING_RAINY: ["28", "29"],
    ATTR_CONDITION_PARTLYCLOUDY: ["2", "3"],
    ATTR_CONDITION_POURING: ["13", "14", "15"],
    ATTR_CONDITION_RAINY: ["8", "9", "10", "11", "12"],
    ATTR_CONDITION_SNOWY: ["22", "23", "24", "25", "26", "27"],
    ATTR_CONDITION_SNOWY_RAINY: ["16", "17", "18"],
    ATTR_CONDITION_SUNNY: ["0", "1"],
    ATTR_CONDITION_WINDY: [],
    ATTR_CONDITION_WINDY_VARIANT: [],
    ATTR_CONDITION_EXCEPTIONAL: [],
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
