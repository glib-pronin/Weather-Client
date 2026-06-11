from pathlib import Path
import dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'

GEONAMES_USERNAME = dotenv.get_key(dotenv_path, 'GEONAMES_USERNAME')