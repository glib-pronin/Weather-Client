from pathlib import Path
import dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'

GEONAMES_USERNAME = dotenv.get_key(dotenv_path, 'GEONAMES_USERNAME')
OPENWEATHER_API_KEY = dotenv.get_key(dotenv_path, 'OPENWEATHER_API_KEY')
WEATHER_API_KEY = dotenv.get_key(dotenv_path, 'WEATHER_API_KEY')