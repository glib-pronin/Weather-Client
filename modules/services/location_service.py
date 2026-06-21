from ..core.config import GEONAMES_USERNAME

class LocationService:
    def __init__(self, api):
        self.api = api
        self.countries = []
        self.selected_country = None
        self.selected_country_code = None
        self.selected_city = None
        self.selected_lat = None
        self.selected_lng = None

    def set_location(self, country, country_code, city, lat, lng):
        self.selected_country = country
        self.selected_country_code = country_code
        self.selected_city = city
        self.selected_lat = lat
        self.selected_lng = lng

    async def load_countries(self):
        if not self.countries:
            res = await self.api.request(
                method='GET',
                url='countries/'
            )
            if res.status_code == 200:
                self.countries = res.json()

    async def save_selection(self, old_data=None):
        if old_data and (
            old_data['city'] == self.selected_city
            and old_data['lat'] == float(self.selected_lat)
            and old_data['lng'] == float(self.selected_lng)
        ):
            return old_data
        res = await self.api.auth_request(
            method='PATCH',
            url='me/',
            json={
                'country': self.selected_country,
                'country_code': self.selected_country_code,
                'city': self.selected_city,
                'lat': self.selected_lat,
                'lng': self.selected_lng,
            }
        )
        if res.status_code == 200:
            return res.json()
        return None

    async def clear_location(self):
        self.set_location(None, None, None, None, None)
        res = await self.save_selection()
        return res
    
    def filter_countries(self, query):
        query = query.strip().lower()
        return [
            country for country in self.countries
            if query in country['name'].lower()
        ]
    
    async def search_cities(self, query):
        print('cities')
        res = await self.api.request(
            method='GET',
            url='http://api.geonames.org/searchJSON',
            params={
                'name_startsWith': query.strip().lower(),
                'country': self.selected_country_code,
                'featureClass': 'P',
                'maxRows': 10,
                'lang': 'uk',
                'orderby': 'population',
                'username': GEONAMES_USERNAME
            }
        )
        if res.status_code != 200:
            return []
        return self._format_cities(res.json())
    
    def _format_cities(self, data):
        cities = []
        for city in data.get('geonames', []):
            name = city['name']
            if ' район' in name:
                continue
            admin = city.get('adminName1')
            
            display_name = name
            # if admin and self.selected_country_code == 'UA':
            if admin:
                display_name = f'{name}, {admin}'

            cities.append({
                'name': name,
                'display_name': display_name,
                'lat': city.get('lat'),
                'lng': city.get('lng')
            })
        return cities
            